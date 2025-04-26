import jax.numpy as jnp
from jax import grad
from jax import jit
import numpy as np

# some constants for RMF
C_CGS    = 29979245800.
hbar     = 6.582119569e-16        #hbar in eV*s
fmi2mev = hbar*C_CGS*1.0e7       #fm^-1 to MeV
m_sigma  = 510.0
m_omega  = 783.0
m_rho    = 770.0
m_nucl   = 939.0
m_e      = 0.511e0
m_mu     = 105.65839

def c3_to_couplings(c3, saturation):
    """
    compute the rest coupling constants with fixed c3 value from the stauration properties
    
    Args:
        c3 (float): The c3 value, must to be positive.
        saturation (array): The saturation properties [n0, E/A, E_sym, K0, J0, M_star]
        
    Returns:
        float: j0, the second derivative of the effective mass with respect to baryon density
        list: The coupling constants [g_sigma, g_omega, g_rho, b_coupling, c_coupling, lambda_v]
    """
    n0     = saturation[0]
    ea     = saturation[1]
    e_sym0 = saturation[2]
    k0     = saturation[3]
    l0     = saturation[4]
    fra_ms = saturation[5]

    m_star     = fra_ms*m_nucl
    n_pro      = n0/2.0
    n_neu      = n_pro
    p_neu_fer  = (3.0*jnp.pi**2*n_neu)**(1.0/3.0)*fmi2mev
    p_pro_fer  = (3.0*jnp.pi**2*n_pro)**(1.0/3.0)*fmi2mev
    e_neu_fer  = jnp.sqrt(p_neu_fer**2 + m_star**2)
    e_pro_fer  = jnp.sqrt(p_pro_fer**2 + m_star**2)
    ns_neu     = m_star*(p_neu_fer*e_neu_fer - m_star**2*jnp.log((p_neu_fer+e_neu_fer)/m_star))/jnp.pi**2/2.0    # MeV
    ns_pro     = m_star*(p_pro_fer*e_pro_fer - m_star**2*jnp.log((p_pro_fer+e_pro_fer)/m_star))/jnp.pi**2/2.0

    # omega field and couplings
    omega = jnp.sqrt((2.0*(ea*n0 - n0*e_neu_fer)*fmi2mev**3)/((jnp.sqrt(4.0*c3*(ea*n0 - n0*e_neu_fer)*fmi2mev**3 + m_omega**4) + m_omega**2)) )
    g_omega = (ea*n0 - n0*e_neu_fer)/omega/n0

    # rho field and couplings
    alpha    = l0 - 3.0*e_sym0 - 0.5*p_neu_fer**2*(g_omega**2*n0*fmi2mev**3/e_neu_fer/(m_omega**2+3.0*c3*omega**2) - k0/e_neu_fer/9.0 - 1.0/3.0)/e_neu_fer
    beta     = 2.0*(e_sym0 - p_neu_fer**2/e_neu_fer/6.0)/n0/fmi2mev**3
    lambda_v = -(m_omega**2 + 3.0*c3*omega**2)*alpha/(3.0*beta**2*g_omega**3*omega*n0**2*fmi2mev**6)
    g_rho    = jnp.sqrt(m_rho**2/(1.0/beta-lambda_v*g_omega**2*omega**2))

    # sigma field and couplings
    dmstar_dpf = (k0 - 3.0*p_neu_fer**2/e_neu_fer - 9.0*g_omega**2/(m_omega**2 + 3.0*c3*omega**2)*n0*fmi2mev**3)*e_neu_fer/m_star/p_neu_fer/3.0
    dns_dms    = (p_neu_fer*e_neu_fer + 2.0*p_neu_fer*m_star**2/e_neu_fer - 3.0*m_star**2*jnp.log((p_neu_fer+e_neu_fer)/m_star))/jnp.pi**2
    A     = ((2.0*p_neu_fer**3 - 3.0*m_star**2*p_neu_fer)*e_neu_fer + 3.0*m_star**4*jnp.log((p_neu_fer+e_neu_fer)/m_star))/ jnp.pi**2/12.0 + 0.5*m_omega**2*omega**2 + c3*omega**4/4.0
    B     = (m_nucl-m_star)*2.0*ns_neu
    C     = -(m_nucl-m_star)**2*(dns_dms + (2.0*m_star*p_neu_fer**2/e_neu_fer)/dmstar_dpf/jnp.pi**2)
    sigma = jnp.sqrt((C-6.0*B+12.0*A)/m_sigma**2)
    g2    = (-3.0*C+15.0*B-24.0*A)/sigma**3
    g3    = (2.0*C-8.0*B+12.0*A)/sigma**4
    g_sigma = (m_nucl-m_star)/sigma

    c_coupling = g3/g_sigma**4
    b_coupling = g2/m_nucl/g_sigma**3

    # compute the second derivative of the effective mass
    dnsp_dpf_dmn = 2*p_neu_fer**4/e_neu_fer**3/dmstar_dpf/jnp.pi**2 + (8*p_neu_fer*m_star/e_neu_fer - 2*p_neu_fer*m_star**3/e_neu_fer**3  \
                                            - 6*m_star*jnp.log((p_neu_fer + e_neu_fer)/m_star) )/jnp.pi**2

    d2mn_b = -2.0*g2-6.0*g3*sigma + 2*g_sigma**3 * (2*m_star*p_neu_fer/e_neu_fer/dmstar_dpf**2 + p_neu_fer**2/e_neu_fer/dmstar_dpf  \
                            - m_star*p_neu_fer**3/e_neu_fer**3/dmstar_dpf**2 - m_star**2*p_neu_fer**2/e_neu_fer**3/dmstar_dpf)/jnp.pi**2  \
                            + g_sigma**3*dnsp_dpf_dmn
    d2mn_a = 2*g_sigma**3 * (m_star*p_neu_fer**2/e_neu_fer/dmstar_dpf**3)/jnp.pi**2
    d2mn = d2mn_b/d2mn_a

    # compute the dk_dnb
    dk_dnb = (6/p_neu_fer/e_neu_fer - 3*p_neu_fer/e_neu_fer**3 - 6*m_star/e_neu_fer**3*dmstar_dpf + 3/p_neu_fer/e_neu_fer*dmstar_dpf**2 \
                + 3*m_star*dmstar_dpf/e_neu_fer/p_neu_fer**2 - 3*m_star**2*dmstar_dpf**2/e_neu_fer**3/p_neu_fer \
                + 3*m_star/p_neu_fer/e_neu_fer*d2mn)*jnp.pi**2/2 + 9*g_omega**2/(m_omega**2 + 3*c3*omega**2) \
                - 54*c3*omega*g_omega**3/(m_omega**2 + 3*c3*omega**2)**3 * n0*fmi2mev**3

    J0 = dk_dnb*fmi2mev**3*3.0*n0 - 12.0*k0

    # d2mn_dn2 = jnp.pi**4*d2mn/p_neu_fer**4/4.0 - jnp.pi**4/p_neu_fer**5/2.0 * dmstar_dpf

    return J0, [g_sigma, g_omega, g_rho, b_coupling, c_coupling, lambda_v]


def sat2couplings(saturation):
    """
    compute the coupling constants from the saturation properties. Using JAX to compute the gradient dJ0/dc3 with automatic differentiation.
    
    Args:
        saturation (array): The saturation properties [n0, E/A, E_sym, K0, J0, M_star, J0]
        
    Returns:
        list: The coupling constants [g_sigma, g_omega, g_rho, b_coupling, c_coupling, lambda_v, c3_omega]
    """
    c3_guess = 2.0e-1  # initial guess for c3, can be tuned
    saturation_no_j0 = jnp.array(saturation[:-1])
    j0_target = saturation[-1]  # target J0 value

    # construct gradient function
    dj0_dc3_f = jit(grad(lambda x: c3_to_couplings(x, saturation)[0]) )

    # find root of C3 to match J0
    c3_root=c3_guess
    for i in range(30):
        f_j0, _ = c3_to_couplings(c3_root, saturation_no_j0)
        df_j0   = dj0_dc3_f(c3_root)
        c3_root = c3_root - (f_j0-j0_target) / df_j0

        if jnp.abs((f_j0 - j0_target)/j0_target) < 1.0e-4:
            break

    if i == 29:
        print("Warning: c3_to_couplings did not converge to the target J0 value within 30 iterations.")

    j0, couplings_no_c3 = c3_to_couplings(c3_root, saturation)
    couplings = [float(x) for x in couplings_no_c3] + [float(c3_root)]

    return couplings
