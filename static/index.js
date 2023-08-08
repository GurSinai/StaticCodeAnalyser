
function getscan(projectname, filename){
    console.log("sdaasdasdasd")
    fetch('/getscan/'+projectname+'/'+filename)
        .then(response => response.json())
        .then(files => {
            const fileContainer = document.getElementById(filename + "-content");
            fileContainer.textContent = files
        })
        .catch(error => console.error('Error fetching files:', error));
}
