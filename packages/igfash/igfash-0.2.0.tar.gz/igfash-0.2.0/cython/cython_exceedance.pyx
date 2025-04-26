# cython: boundscheck=False, wraparound=False, nonecheck=False
import numpy as np
cimport numpy as np
from libc.math cimport log, exp, sqrt, erfc
from scipy.special.cython_special cimport stdtr

cdef inline double normal_sf(double x) nogil:
    return 0.5 * erfc(x / sqrt(2.0))

cdef inline double student_t_sf(double x, int dof) nogil:
    return 1.0 - stdtr(dof, x)

def exceedance_core(
    double a,
    double[:] r,
    double[:] fr,
    double[:] lambdas,
    double D,
    double[:] percentages_D,
    double[:] magnitudes,
    double[:] magnitude_pdf,
    double[:] magnitude_cdf,
    object context_maker,
    object ctx,
    str model,
    int num_ground_motion_records
):
    cdef Py_ssize_t i, j, k, n_events, n_mags
    cdef double exceedance_prob_sum = 0.0
    cdef double log_a = log(a)
    cdef double ri, fr_i, lambda_j, lambda_D_j, denom_j
    cdef double lambda_D_j_f_m, exp_term_m
    cdef double m, f_conditional, log_gm_predicted, variance_term, residual, t_value
    cdef double location_exceedance_prob
    cdef double[:, :, :] mean, sig
    cdef bint is_lasocki = (model == 'Lasocki2013')
    
    n_events = r.shape[0]
    n_mags = magnitudes.shape[0]

    for j in range(lambdas.shape[0]):
        lambda_j = lambdas[j]
        lambda_D_j = lambda_j * D * percentages_D[j]
        denom_j = 1.0 - exp(-lambda_D_j)
        if denom_j == 0.0:
            continue

        for i in range(n_events):
            ri = r[i]
            fr_i = fr[i]
            ctx.repi = ri

            for k in range(n_mags):
                m = magnitudes[k]
                ctx.mag = m
                lambda_D_j_f_m = lambda_D_j * magnitude_pdf[k]
                exp_term_m = exp(-lambda_D_j * (1 - magnitude_cdf[k]))
                f_conditional = (lambda_D_j_f_m * exp_term_m) / denom_j

                mean, sig = context_maker.get_mean_stds(ctx)[:2]
                log_gm_predicted = mean[0, 0, 0]
                variance_term = sig[0, 0, 0]

                residual = log_a - log_gm_predicted
                if residual <= 0:
                    exceedance_probability = 1.0
                else:
                    if variance_term < 1e-15:
                        exceedance_probability = 0.0
                    else:
                        t_value = residual / variance_term
                        if is_lasocki:
                            exceedance_probability = student_t_sf(t_value, num_ground_motion_records - 3)
                        else:
                            exceedance_probability = normal_sf(t_value)

                location_exceedance_prob = exceedance_probability * f_conditional * fr_i
                exceedance_prob_sum += location_exceedance_prob

    return exceedance_prob_sum