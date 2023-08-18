function fill_file_table(fileContainer, projectname, filename, errors, fixes){
    html_addition = " <table class=\"table\"><thead><tr><th scope=\"col\">Error</th><th scope=\"col\">Fix</th></tr></thead><tbody>"
    for (i = 1; i < errors.length; i += 2){
        html_addition += '\n <tr>'
        html_addition += "<td>" + errors[i] + "</td>"
        id = projectname+"/"+filename+"/"+i
        if (!fixes[i]){
            html_addition += "<td id=\"" + id + "\">No fix Available </td>"
        }else{
            html_addition += "<td id=\""+ id +"\">"+atob(fixes[i])+"</td>"
        }
        html_addition += "<td> <a onclick=\"generatefix(\'"+projectname+"\',\'" + mod_filename + "\',\'" + i + "\')\" type=\"a\" class=\"btn btn-info\">Request fix</a></td>"
        html_addition += '\n </tr>'
        
    }
    html_addition += "</tbody></table>"
    fileContainer.innerHTML = html_addition
}

function requestProjectScan(projectname){
    
}

function getscan(projectname, filename){
    mod_filename = filename.replaceAll('/', '-')
    fetch('/getscan/'+projectname+'/'+mod_filename)
        .then(response => response.json())
        .then(errors => {
            fetch('/getfixes/' + projectname + '/' + mod_filename)
                .then(response => response.json())
                .then(fixes => {
                    const fileContainer = document.getElementById(filename + "-content");
                    fill_file_table(fileContainer, projectname, mod_filename, errors, fixes)
                })
        })
        .catch(error => console.error('Error fetching files:', error));
}

function generatefix(projectname, filename, erroridx){
    fetch("/generatefix/"+projectname+"/"+filename+"/" + erroridx)
        .then(response => response.json())
        .then(fix => {
            id = projectname+"/"+filename+"/"+erroridx
            container = document.getElementById(id)
            container.textContent = atob(fix)
            console.log(fix)
        })
        .catch(error => console.error('Error getting fix:', error));
}