function [col_g, col_t] = main2(x_ridge_combined, freq_out, freq, epsilon, dir_out, filen)

    gamma_ridge_combined_fine = map_array_to_gamma(freq_out, freq, x_ridge_combined(3:end), epsilon);


    %gamma_ridge_combined_fine
    #gamma_ridge_combined_coarse = map_array_to_gamma(freq, freq, x_ridge_combined(3:end), epsilon);
    
    rl = x_ridge_combined(1:2)
    col_g = gamma_ridge_combined_fine(:);
    col_t = 1./freq_out(:);
    col_g_1 = rl(1)
    col_t_1 = rl(2)
    whos dir_out
    whos filen
    output = [dir_out "/" filen]
    output
    fid  = fopen(output,'wt');
    fprintf(fid,'%s, %e \n','L',col_g_1);
    fprintf(fid,'%s, %e \n', 'R',col_t_1);
    fprintf(fid,'%s, %s \n','gamma(tau)','tau');
    fprintf(fid,'%e, %e \n', [col_g(:), col_t(:)].');
    fclose(fid);
end