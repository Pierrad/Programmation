// Absolute path to file
var filename = location.pathname
// Cut before "app-darwin-x64" and Get absolute path to the directory where is Electron app and Python code
var filename = filename.substring(0, filename.indexOf("app-darwin-x64"));
// Variable that will be use for test if the 'pathPDF' file is empty or not and after to write PDF
let pathWritingDir;
// Read file and get the path if it exists
var fs = require('fs')
pathPDF = filename + "AutoCompressPDF/pathPDF.txt";
// OutputPy will receive the output from python code
let outputPy = [];

// Listen to event
window.addEventListener('load', function load(event) {

    // Read file and get the path that will be use if we need to write pdf then if it exists display the path else display message to invite creation
    fs.readFile(pathPDF, 'utf8', function(err, data) {
        if (err) throw err;
        pathWritingDir = data;
        if (pathWritingDir != undefined) {
            document.getElementById("actualPath").innerHTML = "Le chemin actuel est : " + pathWritingDir;
        }
        if (pathWritingDir.length == 0){
            document.getElementById("actualPath").innerHTML = "Pas de chemin défini, veuillez en définir un";
        }
    });

    // On click of startbutton
    document.getElementById('startButton').onclick = function(event) {
        // If no path indicate
        if (pathWritingDir.length == 0) {
            // "remote" allows to use electron dialog if we are in renderer process
            let {dialog} = require('electron').remote
            const options = {
                title: 'Attention',
                message: "Le chemin d'accès n'est pas défini, veuillez le définir pour lancer la compression.",
              };
            dialog.showMessageBox(null, options);
        }
        // If path is indicate
        if (pathWritingDir != undefined) {
            // Launch python code
            let {PythonShell} = require('python-shell')
            // Run python code with options and args (the actual absolute path and the path to the PDF file to compress)
            var options = {
                mode: 'text',
                pythonPath: '/usr/local/bin/python3',
                pythonOptions: ['-u'],
                args: [filename, pathWritingDir]
            };
            let pyshell = new PythonShell(filename+'/AutoCompressPDF/autoCompressPDF.py', options);
            // Received a message sent from the Python script (a simple "print" statement)
            pyshell.on('message', function (message) {
                console.log(message);
                outputPy.push(message);
            });
            // End the connexion with the python code
            pyshell.end(function (err,code,signal) {
                if (err) throw err;
            });
            // Display each name file in existingPDF.txt
            for (var i = 0; i < outputPy.length; i++) {
                document.getElementById('myParagraph').insertAdjacentHTML('beforeend', outputPy[i]+"<br>");
            }
        }
    }

    // Click on the button to choose or change the final output path for new PDF File
    document.getElementById('outputDir').onclick = function(event) {
        setTimeout(function(){
            // Get the absolute path for the final output path for new PDF file
            pathWritingDir = document.getElementById("outputDir").files[0].path;
            // Remove the last part '.DS_Store'
            pathWritingDir = pathWritingDir.substring(0, pathWritingDir.indexOf(".DS_Store"));
            // Rewrite ou replace the path in the file
            fs.writeFile(pathPDF, pathWritingDir, function(err) {
                if (err) throw err;
            });
            // If no path at the beginning there was a message but if we choose a path we remove this message
            if (document.getElementById("actualPath").innerHTML == "Pas de chemin défini, veuillez en définir un") {
                document.getElementById("actualPath").innerHTML = "";
            }
            // Define the pathWritingDir that will be send to the python code
            document.getElementById('MessageLaunchCompression').innerHTML = "Vous pouvez lancer la compression!";
        }, 10000);
    }
})