var sentenceIndex = 0;
var wordIndex = 0;

function addinput(div, title, contents) {
    div.innerHTML += title + ": ";
    input = document.createElement('input');
    input.setAttribute('type', 'text');
    input.setAttribute('style', 'width: 80%');
    if(contents !== undefined)
        input.setAttribute('value', contents);
    div.appendChild(input);
}

function addsentence(expression, meaning, reading, audio) {
    sentenceDiv = document.createElement('div');
    sentenceDiv.setAttribute('id', "sentence" + sentenceIndex);
    sentenceDiv.innerHTML += "<hr/>";

    sentenceDiv.innerHTML += "<br />";

    addinput(sentenceDiv, "Expression", expression);
    sentenceDiv.innerHTML += "<br />";

    addinput(sentenceDiv, "Meaning", meaning);
    sentenceDiv.innerHTML += "<br />";

    addinput(sentenceDiv, "Reading", reading);
    sentenceDiv.innerHTML += "<br />";

    addinput(sentenceDiv, "Audio", audio);
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
    removeItem('word' + wordIndex);
    onFormChange();
}

function removeAllSentences() {
    for(var i=0;i<sentenceIndex;i++) {
        removeItem('sentence' + i)
    }
    sentenceIndex = 0;
    onFormChange();
}

function onInputChange() {
    blockInput = document.getElementById('blockInput');
    removeAllSentences();
    items = blockInput.value.split("\n");
    for(var i=0;i<items.length;i++) {
        parts = items[i].split("\t");
        if(parts.length >= 4)
            addsentence(parts[1], parts[0], parts[2], parts[3]);
    }
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
    wordDivs = sentenceDiv.getElementsByTagName('div');
    for(var i=0;i<wordDivs.length;i++) {
        inputs = wordDivs[i].getElementsByTagName('input');
        // get inputs
        word = inputs[0].value;
        wordMeaning = inputs[1].value;
        wordReading = getReading(word, reading);

        // make word card
        output.innerHTML += "a one piece of info::b writing and meaning -> reading (words)"
        output.innerHTML += "\t";
        output.innerHTML += "Japanese writing and meaning -> reading (words)"
        output.innerHTML += "\t";
        output.innerHTML += "0"
        output.innerHTML += "\t";
        output.innerHTML += word;
        output.innerHTML += "\t";
        output.innerHTML += wordMeaning;
        output.innerHTML += "\t";
        output.innerHTML += getContext(word, reading);
        output.innerHTML += "\t";
        output.innerHTML += wordReading;
        output.innerHTML += "\n";

        // make kanji cards
        kanjis = split(word);
        for(var j=0;j<kanjis.length;j++) {
            kanji = kanjis[j];
            if(is_kana_or_english(kanji)) continue;
            output.innerHTML += "a one piece of info::a meaning and reading -> writing (kanji)";
            output.innerHTML += "\t";
            output.innerHTML += "Japanese meaning and reading -> stroke order (kanji)";
            output.innerHTML += "\t";
            output.innerHTML += "0";
            output.innerHTML += "\t";
            output.innerHTML += cloze(kanji, wordReading);
            output.innerHTML += "\t";
            output.innerHTML += kanji;
            output.innerHTML += "\t";
            output.innerHTML += wordMeaning;
            output.innerHTML += "\t";
            output.innerHTML += cloze(kanji, reading);
            output.innerHTML += "\n";
        }
    }
}

function split(word) {
    return word.split("");
}

function is_kana_or_english(ch) {
    // http://stackoverflow.com/questions/15033196/using-javascript-to-check-whether-a-string-contains-japanese-characters-includi
    if(ch.match(/[\u3040-\u309f\u30a0-\u30ff]/)) return true;
    if(ch.match(/[\[\]]/)) return true;
    return false;
}

function getContext(word, sentence_reading) {
    // return the sentence reading with the word's reading removed
    search = getReading(word, sentence_reading);
    if(sentence_reading.indexOf(" " + search) > -1) {
        return sentence_reading.replace(" " + search, word);
    }
    return sentence_reading.replace(search, word);
}

function getReading(word, sentence_reading) {
    // return the word with reading attached
    regex = "";
    kanjis = split(word);
    for(var i=0;i<kanjis.length;i++) {
        if(i>0) regex += '\\s*';
        regex += kanjis[i] + '(?:\\[[^\\]]+\\])?';
    }
    regex = new RegExp(regex);
    matches = regex.exec(sentence_reading);
    result = matches[0];
    return result;
}

function cloze(kanji, str) {
    // replace kanji with full-width _ in string
    return str.replace(kanji, "\uFF3F");
}
