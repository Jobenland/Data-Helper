function [H_combined, f_combined, freq_out, freq, epsilon] = main(fullFileName, lambda)
#function [col_g, col_t] = main(fullFileName)
    A=csvread(fullFileName);
    
    freq = A(:,1);
    Z_prime_mat = A(:,2);
    Z_double_prime_mat = A(:,3);
    data_exist=1;
    #lambda = 6.5e-3;
    
    rbf_gaussian_4_FWHM = @(x) exp(-(x).^2)-1/2;  %okay
    FWHM_gaussian = 2*fzero(@(x) rbf_gaussian_4_FWHM(x), 1); %okay
    FWHM_coeff = FWHM_gaussian % okay
    
    Z_prime_mat = A(:,2);
    Z_double_prime_mat = A(:,3);
    data_exist=1;
    
    
    rbf_gaussian_4_FWHM = @(x) exp(-(x).^2)-1/2;  %okay
    FWHM_gaussian = 2*fzero(@(x) rbf_gaussian_4_FWHM(x), 1); %okay
    FWHM_coeff = FWHM_gaussian % okay

    coeff = 0.5 % okay
    #options = optimset('algorithm','interior-point-convex','Display','off','TolFun',1e-15,'TolX',1e-10,'MaxFunEvals', 1E5)

    
    lb_im = zeros(numel(freq)+2,1);
    ub_im = Inf*ones(numel(freq)+2,1);
    x_im_0 = zeros(size(lb_im));
    lb_re = zeros(numel(freq)+2,1);
    ub_re = Inf*ones(numel(freq)+2,1);
    x_re_0 = ones(size(lb_re));
    taumax=ceil(max(log10(1./freq)))+1; %% is it good enough??     
    taumin=floor(min(log10(1./freq)))-1;

    
    delta = mean(diff(log(1./freq))); 

    
    epsilon  = coeff*FWHM_coeff/delta;

    freq_o=freq;

    
    freq_out = logspace(-taumin, -taumax, 10*numel(freq));

    Z_prime_mat_o=Z_prime_mat;
    Z_double_prime_mat_o=Z_double_prime_mat;

    
    Z_exp = Z_prime_mat(:)+ i*Z_double_prime_mat(:);

    
    b_re = real(Z_exp);
    b_im = -imag(Z_exp);
    
    
    
    a_re = assemble_A_re(freq, epsilon);
    
    a_im = assemble_A_im(freq, epsilon, 0);
    
    
    m_re = assemble_M_re(freq, epsilon);
    
    m_im = assemble_M_im(freq, epsilon);
    

    %Should be good
    #optio = optimset('MaxIter', 10000)
    [H_combined,f_combined] = quad_format_combined(a_re, a_im, b_re, b_im, m_re, m_im, lambda);

    #H_combined
    f1_combined = f_combined;
    #options = optimoptions('algorithm','interior-point-convex','TolFun',1e-15,'TolX',1e-10,'MaxFunEvals', 1E5)
    options = optimset('MaxIter', 1E5)
    fullFileName
    #[x_ridge_combined, fval, exitflag, output, lambda] = quadprog(H_combined, f1_combined, [], [], [], [],  lb_re, ub_re);
    #x_ridge_combined = lambda.lower;
    #
    #
    #gamma_ridge_combined_fine = map_array_to_gamma(freq_out, freq, x_ridge_combined(3:end), epsilon);
#
    #col_g = gamma_ridge_combined_fine(:);
    #col_t = 1./freq_out(:);
    
    
    #[x_ridge_combined, fval, exitflag]  = quadprog(H_combined, f_combined)
    #exitflag
    #obj
    %DIFFERENT DATA FROM ORIGINAL  -Slightly different code from original from original
 end  
