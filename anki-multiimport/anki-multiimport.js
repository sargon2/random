var sentenceIndex = 0;
function addsentence() {
    d = document.createElement('div');
    d.setAttribute('id', sentenceIndex);

    i = document.createElement('input');
    i.setAttribute('type', 'text');
    d.appendChild(i);

    r = document.createElement('button');
    r.setAttribute('onclick', 'removesentence(' + sentenceIndex + ')');
    r.setAttribute('type', 'button');
    r.innerHTML = "remove sentence";

    d.appendChild(r);
    document.getElementById("myForm").appendChild(d);
    sentenceIndex++;
}

function removesentence(sentenceIndex) {
    document.getElementById("myForm").removeChild(document.getElementById(sentenceIndex));
}
