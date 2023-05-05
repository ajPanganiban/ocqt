function c_cell=to_cell(mat)
    coef1 = num2cell(mat,2);
    coef2 = cellfun(@transpose,coef1,'UniformOutput',false);
    c_cell = coef2;
end