function matlab2opencv( variable, fileName, flag)
 
[rows, cols] = size(variable);
 
% Beware of Matlab's linear indexing
variable = variable';
 
% Write mode as default
if ( ~exist('flag','var') )
    flag = 'w';
end
 
if ( ~exist(fileName,'file') || flag == 'w' )
    % New file or write mode specified
    file = fopen( fileName, 'w');
    fprintf( file, '%%YAML:1.0\n');
else
    % Append mode
    file = fopen( fileName, 'a');
end

if rows==1 && cols==1
    fprintf( file, '    %s: ', inputname(1));
    fprintf( file, '%.6f\n', variable);
else
    % Write variable header
    fprintf( file, '    %s: !!opencv-matrix\n', inputname(1));
    fprintf( file, '        rows: %d\n', rows);
    fprintf( file, '        cols: %d\n', cols);
    fprintf( file, '        dt: f\n');
    fprintf( file, '        data: [ ');
     
    % Write variable data
    for i=1:rows*cols
        fprintf( file, '%.6f', variable(i));
        if (i == rows*cols), break, end
        fprintf( file, ', ');
        if mod(i+1,4) == 0
            fprintf( file, '\n            ');
        end
    end
    fprintf( file, ']\n');
end
 

 
fclose(file);