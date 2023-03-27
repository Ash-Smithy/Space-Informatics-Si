const button = document.getElementById('send');
var userInp = document.getElementById('userInp');


button.addEventListener('click', (e) => {
     display(userInp.value);
     userInp.reset;
});

/*function getdata(data) {
    fetch("/get-data", {
    method: "POST",
    body: JSON.stringify({ data: data }),
    }).then((_res) => {
    window.location.href = "/bot";
    });
}*/

function display(val) {
   /* var userDiv = document.createElement('div'); //Create  a division
    var userP = document.createElement('p'); // create a pratagraph
    var userMsg = document.getElementById('userMsg'); //Send the message to the paragraph
    var msg = document.createTextNode(val);
    userDiv.appendChild(userP);
    userP.appendChild(msg);
    userMsg.appendChild(userDiv);
    console.log(userInp.value);*/

};


