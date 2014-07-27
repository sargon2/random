var sentenceIndex = 0;
var wordIndex = 0;

function addinput(div, title) {
    div.innerHTML += title + ": ";
    input = document.createElement('input');
    input.setAttribute('type', 'text');
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
}

function removesentence(sentenceIndex) {
    // TODO: "are you sure?"
    removeItem('sentence' + sentenceIndex);
}
