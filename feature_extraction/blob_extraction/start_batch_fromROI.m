%start_batch_tamu.m
%configure and initiate batch processing for blob extractiom

in_dir= 'C:\work\IFCB\test\data\'; %USER 
out_dir = 'C:\work\IFCB\test\data\blobs\'; %USER main blob output location

bins = dir([in_dir '*.adc']);
bins = regexprep({bins.name}', '.adc', '');

for bincount = 1:length(bins),
    disp(bins{bincount})
    png_path = [in_dir bins{bincount}  filesep];
    blob_png_path = [out_dir bins{bincount}  filesep];
    if ~exist('blob_png_path', 'dir'),
        mkdir(blob_png_path)
    end;
    [targets, imglist] = get_images_fromROI([in_dir bins{bincount} '.roi']);
    disp('    writing blobs...')
    for i = 1:length(imglist),
        target = {};
        % configure feature extraction
        target.config = configure();
        % get the image
        target.image = cell2mat(targets.image(i));
        % compute the blob mask (result in target.blob_image)
        target = blob(target);
        % now output the blob image as a 1-bit png
        imwrite(target.blob_image,[blob_png_path imglist{i} '.png'],'bitdepth',1);
    end;
end

