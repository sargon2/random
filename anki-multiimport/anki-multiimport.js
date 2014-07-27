var sentenceIndex = 0;
var wordIndex = 0;

function addinput(div, title) {
    div.innerHTML += title + ": ";
    input = document.createElement('input');
    input.setAttribute('type', 'text');
    // TODO: better layout
    input.setAttribute('style', 'width: 80%');
    div.appendChild(input);
}

function addsentence() {
    sentenceDiv = document.createElement('div');
    sentenceDiv.setAttribute('id', "sentence" + sentenceIndex);
    sentenceDiv.innerHTML += "<hr/>";

    removeSentenceButton = document.createElement('button');
    removeSentenceButton.setAttribute('onclick', 'removesentence(' + sentenceIndex + ')');
    removeSentenceButton.setAttribute('type', 'button');
    removeSentenceButton.innerHTML = "remove sentence";
    sentenceDiv.appendChild(removeSentenceButton);

    sentenceDiv.innerHTML += "<br />";

    addinput(sentenceDiv, "Expression");
    sentenceDiv.innerHTML += "<br />";

    addinput(sentenceDiv, "Meaning");
    sentenceDiv.innerHTML += "<br />";

    addinput(sentenceDiv, "Reading");
    sentenceDiv.innerHTML += "<br />";

    addinput(sentenceDiv, "Audio");
    sentenceDiv.innerHTML += "<br />";

    addWordButton = document.createElement('button');
    addWordButton.setAttribute('onclick', 'addword(' + sentenceIndex + ')');
    addWordButton.setAttribute('type', 'button');
    addWordButton.innerHTML = "Add word";
    sentenceDiv.appendChild(addWordButton);

    document.getElementById("myForm").appendChild(sentenceDiv);
    sentenceIndex++;
}

function addword(sentenceIndex) {
    wordDiv = document.createElement('div');
    wordDiv.setAttribute('id', "word" + wordIndex);

    addinput(wordDiv, "Word");
    wordDiv.innerHTML += "<br />";

    addinput(wordDiv, "Meaning");
    wordDiv.innerHTML += "<br />";

    addinput(wordDiv, "Context");
    wordDiv.innerHTML += "<br />";

    addinput(wordDiv, "Reading");
    wordDiv.innerHTML += "<br />";

    removeWordButton = document.createElement('button');
    removeWordButton.setAttribute('onclick', 'removeword(' + wordIndex + ')');
    removeWordButton.setAttribute('type', 'button');
    removeWordButton.innerHTML = "remove word";
    wordDiv.appendChild(removeWordButton);

    sentenceDiv = document.getElementById('sentence' + sentenceIndex);
    sentenceDiv.appendChild(wordDiv);
    wordIndex++;
}

function removeItem(id) {
    div = document.getElementById(id);
    div.parentNode.removeChild(div);
}

function removeword(wordIndex) {
    // TODO: "are you sure?"
    removeItem('word' + wordIndex);
    onFormChange();
}

function removesentence(sentenceIndex) {
    // TODO: "are you sure?"
    removeItem('sentence' + sentenceIndex);
    onFormChange();
}

function onFormChange() {
    output = document.getElementById('output');
    output.innerHTML = "";
    // for each sentence
    var nodes = document.getElementById('myForm').childNodes;
    for(var i=0;i<nodes.length;i++) {
        sentenceDiv = nodes[i];
        if(sentenceDiv.nodeType != 1) continue;
        addSentence(sentenceDiv);
    }
}

function addSentence(sentenceDiv) {
    // for each input
    inputs = sentenceDiv.getElementsByTagName('input');
    expression = inputs[0].value;
    meaning = inputs[1].value;
    reading = inputs[2].value;
    audio = inputs[3].value;

    output.innerHTML += "a one piece of info::c writing and reading -> meaning (sentences)";
    output.innerHTML += "\t";
    output.innerHTML += "Japanese stroke order and reading -> meaning (sentences)";
    output.innerHTML += "\t";
    output.innerHTML += "0";
    output.innerHTML += "\t";
    output.innerHTML += expression + "\t" + meaning + "\t" + reading + "\t" + audio;
    output.innerHTML += "\n";

    // for each word div
    // get inputs
    // make word card
    // make kanji cards, if not kana
}
