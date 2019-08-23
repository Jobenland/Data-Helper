function out_val = g_ii(freq_n, freq_m, epsilon)

alpha = 2*pi*freq_n/freq_m;
rbf = @(x) exp(-(epsilon*x).^2);

integrand_g_ii = @(x) (2*pi*freq_n/freq_m)./(1./exp(x)+(2*pi*freq_n/freq_m)^2*exp(x)).*exp(-(epsilon*x).^2);

quad_options('absolute tolerance', 1e6);
quad_options('relative tolerance', 1e6);
quad_options('single precision relative tolerance', 1e6);
quad_options('single precision absolute tolerance', 1e6);
out_val = quadcc(integrand_g_ii, -Inf, Inf);



end