function [] = SelectObjResult(obj_dir, save_dir)
    obj_list = dir(fullfile(obj_dir, '*.obj'));
    if nargin < 2
        save_dir = [obj_dir,'\sel'];
    end
    if ~exist(save_dir, 'dir')
        mkdir(save_dir)
    end
    fig = figure;
    i = 1;
    while i < size(obj_list, 1)
        obj_name = fullfile(obj_dir, obj_list(i).name);
        [v, f] = readobjfromfile(obj_name);
        f = f + 1;
        v([1,2,3]) = v([3,1,2]);
        face_color = repmat([0.5, 0.5, 0.5],size(v,1),1);
        patch('Faces',f,'Vertices',v, 'FaceVertexCData',face_color, 'FaceColor','b', 'EdgeColor', 'none');
        title(obj_list(i).name)
        axis equal;
        hold on;
        lighting phong;
        camlight('left');
        camlight('right')
        lighting phong;
        material metal
        camlight infinite;
        shading interp;
        view(-152, -61);
        w = waitforbuttonpress;
        if fig.CurrentCharacter == 's'
            copyfile(fullfile(obj_dir, obj_list(i).name),fullfile(save_dir,obj_list(i).name))
            fprintf('save %s!\n', obj_list(i).name);
        elseif fig.CurrentCharacter == 'f'
            i = i + 1;
        elseif fig.CurrentCharacter == 'a'
            i = i - 1;
        elseif fig.CurrentCharacter == 'd'
            delete(fullfile(save_dir,obj_list(i).name))
            fprintf('delete %s!\n', obj_list(i).name);
        elseif fig.CurrentCharacter == 'q'
            close(gcf)
            break;
        end
        cla;
    end
    close(gcf)

end


