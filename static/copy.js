function copying(){
    const cb = navigator.clipboard;
    var copyText = document.getElementById("links");
    var button1=document.getElementById("copys");
    const paragraph = document.querySelector('p');
    cb.writeText(paragraph.innerText).then(() => button1.textContent="text copied !");
}