function deleteNote(noteId){
    //prende la noteId ^
    fetch('/delete-note',{
        method: 'POST', //fa una post request a /delete-note e quando riceve risposta ->
        body: JSON.stringify({ notrId: noteId}),
    }).then((_res) => { //refresha la pagina.
        window.location.href="/";
    });
}