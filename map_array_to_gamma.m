function out_gamma = map_array_to_gamma(freq_map, freq_coll, x, epsilon)

% choose among positive definite RBFs
% rbf refer to the phi function. On multiply phi function with x, the
% magnitude at the specific frequency, one can give the gamma profile
% choose a function from a switch

x = x.'
rbf = @(y, y0) exp(-(epsilon*(y-y0)).^2);

y0 = -log(freq_coll);
out_gamma = zeros(size(freq_map));

for iter_freq_map = 1: numel(freq_map)

    freq_map_loc = freq_map(iter_freq_map);
    y = -log(freq_map_loc);
    out_gamma(iter_freq_map) = x'*rbf(y, y0);

end

end