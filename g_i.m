function out_val = g_i(freq_n, freq_m, epsilon)

#alpha = 2*pi*freq_n/freq_m;
#rbf = @(x) exp(-(epsilon*x).^2);
% choose among positive definite RBFs
% choose a function from a switch
% end of switch


integrand_g_i = @(x) 1./(1+(2*pi*freq_n/freq_m)^2*exp(2*x)).*exp(-(epsilon*x).^2);

quad_options('absolute tolerance', 1e9)
quad_options('relative tolerance', 1e9)
quad_options('single precision relative tolerance', 1e9)
quad_options('single precision absolute tolerance', 1e9)
out_val = quadcc(integrand_g_i, -Inf, Inf);



end