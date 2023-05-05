function [c_mat,row,col]=to_mat(cells)
    [x, row] = size(cells);
    c1 = cellfun(@transpose,cells,'UniformOutput',false);
    [x, col] = size(c1{1});
    c2 = cell2mat(c1);
    c_mat = c2;
end