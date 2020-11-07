/* imports */
var execSync = require('exec-sync');
var util = require('util');
var fs = require('fs');
var s3 = require('s3');
var keychain = require('keychain');

/* config */
var config = {
    output_folder: "transcoder_output",
    audio_file_name: "transcoder_output/audio.mp3",
    image_file_name: "transcoder_output/image_%05d.jpg",
    aws_name: "AKIAIG2ODXQTVB5HGGLQ",
    bucket_name: "jpgs.videopath.com"
};


var result;

var filename = process.argv[2];
var video_key = process.argv[3];

/* check existense of arguments */
if (!filename) {
    console.log("Please specify filename. Usage: \"node transcoder.js <filename> <videokey>\".")
    return;
}

if (!video_key) {
    console.log("Please specify video key. Usage: \"node transcoder.js <filename> <videokey>\".")
    return;
}

// create output folder
execSync('rm -rf ' + config.output_folder);
fs.mkdirSync(config.output_folder);

// convert audio
/*
console.log("=== Converting Audio ===");
try {
    result = execSync("ffmpeg -i " + filename + " -b:a 192k -map a " + config.audio_file_name);
} catch (ignore) {}


// convert images
console.log("=== Converting Images ===");
try {
    result = execSync("ffmpeg -i " + filename + " -r 25 -vf scale=640:-1 -q:v 15 -an -f image2 " + config.image_file_name);
} catch (ignore) {}
*/

function finalize() {
    execSync('rm -rf ' + config.output_folder);
    console.log("=== Done ===");
}

// upload to s3
keychain.getPassword({
    account: config.aws_name,
    kind: "application password",
    service: "vp aws"
}, function(err, pass) {

    pass = "sz5HWoVSN9aG9n4/i+JRa0uUlo+NVez8u2BXaNPI";

    // connect to s3
    var client = s3.createClient({
        s3Options: {
            accessKeyId: config.aws_name,
            secretAccessKey: pass,
            region: "eu-west-1",
            maxAsyncS3: 5,
        }
    });

    var count = 0;
    var files = fs.readdirSync(config.output_folder);
    uploadNext = function() {

        var fileName = files[count];
        count++;

        if (!fileName) {
            return;
        }

        var percent = 0;

        // upload files
        var params = {
            localFile: config.output_folder + "/" + fileName,

            s3Params: {
                Bucket: config.bucket_name,
                Key: video_key + "/" + fileName,
                ACL: "public-read"
            },
        };
        var uploader = client.uploadFile(params);
        uploader.on('error', function(err) {
            console.log("Error Uploading " + fileName);
        });
        uploader.on('end', function() {
            console.log("Done Uploading " + fileName);
            uploadNext();
        });

    }

    uploadNext();


});