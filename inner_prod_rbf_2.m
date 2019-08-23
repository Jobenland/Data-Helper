function out_IP = inner_prod_rbf_2(freq_n, freq_m, epsilon, rbf_type)

a = epsilon*log(freq_n/freq_m);
out_IP = epsilon^3*(3-6*a^2+a^4)*exp(-(a^2/2))*sqrt(pi/2);

% % begin integrate test:
% y_n = -log(freq_n);
% y_m = -log(freq_m);
% 
% switch rbf_type
%     case 'gaussian'
%         rbf_n = @(y) exp(-(epsilon*(y-y_n)).^2);
%         rbf_m = @(y) exp(-(epsilon*(y-y_m)).^2);
%         
%     case 'C0_matern'
%         rbf_n = @(y)  exp(-abs(epsilon*(y-y_n)));
%         rbf_m = @(y)  exp(-abs(epsilon*(y-y_m)));
%         
%     case 'C2_matern'
%         rbf_n = @(y)  exp(-abs(epsilon*(y-y_n))).*(1+abs(epsilon*(y-y_n)));
%         rbf_m = @(y)  exp(-abs(epsilon*(y-y_m))).*(1+abs(epsilon*(y-y_m)));
%         
%     case 'C4_matern'
%         rbf_n = @(y)  exp(-abs(epsilon*(y-y_n))).*(3+3*abs(epsilon*(y-y_n))+abs(epsilon*(y-y_n)).^2);
%         rbf_m = @(y)  exp(-abs(epsilon*(y-y_m))).*(3+3*abs(epsilon*(y-y_m))+abs(epsilon*(y-y_m)).^2);
%         
%     case 'C6_matern'
%         rbf_n = @(y)  exp(-abs(epsilon*(y-y_n))).*(15+15*abs(epsilon*(y-y_n))+6*abs(epsilon*(y-y_n)).^2+abs(epsilon*(y-y_n)).^3);
%         rbf_m = @(y)  exp(-abs(epsilon*(y-y_m))).*(15+15*abs(epsilon*(y-y_m))+6*abs(epsilon*(y-y_m)).^2+abs(epsilon*(y-y_m)).^3);
%         
%     case 'inverse_quadratic'
%         rbf_n = @(y) 1./(1+(epsilon*(y-y_n)).^2);
%         rbf_m = @(y) 1./(1+(epsilon*(y-y_m)).^2);
%         
%     case 'inverse_quadric'
%         rbf_n = @(y) 1./sqrt(1+(epsilon*(y-y_n)).^2);
%         rbf_m = @(y) 1./sqrt(1+(epsilon*(y-y_m)).^2);
%         
%     case 'cauchy'
%         rbf_n = @(y) 1./(1+abs(epsilon*(y-y_n)));
%         rbf_m = @(y) 1./(1+abs(epsilon*(y-y_m)));
%         
%     otherwise
%         warning('Unexpected RBF input');
%         
% end
% % end of switch
% 
% % compute derivative
% delta = 1E-4;
% sqr_drbf_dy = @(y) 1/(delta^2).*(rbf_n(y+delta)-2*rbf_n(y)+rbf_n(y-delta)).*1/(delta^2).*(rbf_m(y+delta)-2*rbf_m(y)+rbf_m(y-delta));
% % y_dummy = linspace(-10, 10, 10001);
% % plot(y_dummy,sqr_drbf_dy(y_dummy));
% 
% out_IP2 = integral(@(y) sqr_drbf_dy(y),-Inf,Inf);
% 
% fprintf('absolute error = %e \n', abs(out_IP- out_IP2));
% fprintf('rel error = %f percent \n', 100*abs(out_IP- out_IP2)/abs(out_IP));
% if abs(out_IP- out_IP2)/abs(out_IP)>1E-2 pause();end
% % end test

end
