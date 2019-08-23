function out_M_im = assemble_M_im(freq, epsilon)

% This is the matrix of all inner products 
% of the RBF elements
std_freq = std(diff(log(1./freq)));
mean_freq = mean(diff(log(1./freq)));
R=zeros(1,numel(freq));
C=zeros(numel(freq),1);
out_M_im_temp = zeros(numel(freq));
out_M_im = zeros(numel(freq)+2, numel(freq)+2);

    
        if std_freq/mean_freq<1  %(error in frequency difference <1% make sure that the terms are evenly distributed)
            for iter_freq_n = 1: numel(freq)
                
                    freq_n = freq(iter_freq_n);
                    freq_m = freq(1);
                    C(iter_freq_n, 1) = inner_prod_rbf(freq_n, freq_m, epsilon);
                    
            end  

            for iter_freq_m = 1: numel(freq)

                    freq_n = freq(1);
                    freq_m = freq(iter_freq_m);
                    R(1, iter_freq_m) = inner_prod_rbf(freq_n, freq_m, epsilon);

            end

            out_M_im_temp = toeplitz(C,R);

        else %if log of tau is not evenly distributed

            for iter_freq_n = 1: numel(freq)

                for iter_freq_m = 1: numel(freq)

                    freq_n = freq(iter_freq_n);
                    freq_m = freq(iter_freq_m);
                    out_M_im_temp(iter_freq_n, iter_freq_m) = inner_prod_rbf(freq_n, freq_m, epsilon);

                end
            end
        end

        
    
    


out_M_im(3:end, 3:end) = out_M_im_temp;

end

