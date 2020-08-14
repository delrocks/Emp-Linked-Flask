var id;
var i = 1;

$(document).ready(function () {
  document.getElementById("saveButton").onclick = function () {
    if (CheckNote("notename", "notecontent")) {
      var element = CreateNote();
      element.setAttribute("id", i++);
      var insert = document.getElementById("container");

      if (insert != null)
        insert.insertBefore(element, insert.firstChild);
      else
        document.getElementById("container").appendChild(element);
      return false;
    }
    return true;
  };

  document.getElementById("deleteButton").onclick = function () {
    var toRemove = document.getElementById(id);
    toRemove.parentElement.removeChild(toRemove);

    var insert = document.getElementById("deteledContainer");

    if (insert != null)
      insert.insertBefore(toRemove, insert.firstChild);
    else
      document.getElementById("deletedContainer").appendChild(toRemove);

    document.getElementById("g0" + toRemove.id).remove();
    document.getElementById("g1" + toRemove.id).remove();
    document.getElementById("g2" + toRemove.id).remove();
    document.getElementById("glyphContainer" + toRemove.id).appendChild(RestoreGlyph(toRemove.id));

    toRemove.className += " grayout";
  };

  document.getElementById("yesButton").onclick = function () {
    var toMove = document.getElementById(id);
    toMove.parentElement.removeChild(toMove);
    toMove.className += " grayout";

    document.getElementById("container").appendChild(toMove);
    var glyph = document.getElementById("g1" + toMove.id);
    glyph.removeAttribute("data-toggle");
    glyph.removeAttribute("data-target");
  };

  document.getElementById("restoreYes").onclick = function () {
    var toMove = document.getElementById(id);
    toMove.parentElement.removeChild(toMove);
    toMove.className = "col-sm-4 margin";

    var insert = document.getElementById("container");

    if (insert != null)
      insert.insertBefore(toMove, insert.firstChild);
    else
      document.getElementById("container").appendChild(toMove);

    document.getElementById("g3" + toMove.id).remove();
    var cont = document.createElement("div");
    cont.style.position = "absolute";
    cont.style.bottom = "0";
    cont.style.right = "0";
    cont.style.marginRight = "5px";
    cont.style.marginBottom = "5px";
    cont.appendChild(YesGlyph(toMove.id));
    cont.appendChild(NoGlyph(toMove.id));

    document.getElementById("glyphContainer" + toMove.id).insertBefore(EditGlyph(toMove.id), document.getElementById("glyphContainer" + toMove.id).firstChild);
    document.getElementById("glyphContainer" + toMove.id).appendChild(cont);
  };

  document.getElementById("editButton").onclick = function () {
    if (CheckNote("editname", "editcontent")) {
      var newTitle = document.getElementById("heading" + id);
      newTitle.textContent = document.getElementById("editname").value;

      var newBody = document.getElementById("glyphContainer" + id);
      newBody.textContent = document.getElementById("editcontent").value;
      newBody.innerHTML += '<br/><br/>';

      if (newBody.parentElement.parentElement.parentElement.id == "container")
        newBody = createGlyphs(newBody, id);
      else {
        newBody.appendChild(RestoreGlyph(id));
      }
      return false;
    };
    return true;
  };

  document.getElementById("notecontent").onkeypress = function (e) {
    if (e.keyCode == 13)
      document.getElementById("saveButton").click();
  };
});

function YesGlyph(currentId) {
  var span1 = document.createElement("span");
  span1.className = "glyphicon glyphicon-ok pull-right";
  span1.setAttribute("id", 'g1' + currentId);
  span1.setAttribute("onclick", "okGlyphInDiv(this)");
  span1.setAttribute("data-toggle", "modal");
  span1.setAttribute("data-target", "#okModal");
  return span1;
};

function NoGlyph(currentId) {
  var span2 = document.createElement("span");
  span2.className = "glyphicon glyphicon-remove pull-right";
  span2.setAttribute("id", 'g2' + currentId);
  span2.setAttribute("onclick", "okGlyphInDiv(this)");
  span2.setAttribute("data-toggle", "modal");
  span2.setAttribute("data-target", "#deleteModal");
  return span2;
};

function RestoreGlyph(currentId) {
  var glyph = document.createElement("span");
  glyph.className = "glyphicon glyphicon-refresh pull-right";
  glyph.setAttribute("id", 'g3' + currentId);
  glyph.setAttribute("onclick", "okGlyph(this)");
  glyph.setAttribute("data-toggle", "modal");
  glyph.setAttribute("data-target", "#restoreModal");
  glyph.style.position = "absolute";
  glyph.style.top = "initial";
  glyph.style.bottom = "0";
  glyph.style.right = "0";
  glyph.style.marginRight = "5px";
  glyph.style.marginBottom = "5px";
  return glyph;
};

function EditGlyph(currentId) {
  var glyph = document.createElement("span");
  glyph.className = "glyphicon glyphicon-edit pull-right";
  glyph.setAttribute("id", 'g0' + currentId);
  glyph.setAttribute("onclick", "okGlyph(this)");
  glyph.setAttribute("data-toggle", "modal");
  glyph.setAttribute("data-target", "#editModal");
  glyph.style.position = "absolute";
  glyph.style.top = "0";
  glyph.style.right = "0";
  glyph.style.marginRight = "5px";
  glyph.style.marginTop = "5px";

  return glyph;
};

function okGlyph(that) {
  id = that.parentElement.parentElement.parentElement.id;
};

function okGlyphInDiv(that) {
  id = that.parentElement.parentElement.parentElement.parentElement.id;
};

function CreateNote() {
  var note = document.createElement("div");
  note.className = "col-sm-4 margin";
  note.setAttribute("id", "notehover");
  var panel = document.createElement("div");
  panel.className = "panel panel-default";
  panel.style.height = "200px";
  var heading = document.createElement("div");
  heading.className = "panel-body headingcolor";
  heading.setAttribute("id", "heading" + i);
  heading.textContent = document.getElementById("notename").value;
  var body = document.createElement("div");
  body.className = "panel-body";
  body.setAttribute("id", "glyphContainer" + i);
  body.style.overflow = "hidden";
  body.style.position = "relative";
  body.style.height = "73%";
  body.textContent = document.getElementById("notecontent").value;
  body.innerHTML += '<br/><br/>';
  body = createGlyphs(body, i);
  panel.appendChild(heading);
  panel.appendChild(body);
  note.appendChild(panel);
  return note;
};

function createGlyphs(body, id) {
  var cont = document.createElement("div");
  cont.style.position = "absolute";
  cont.style.bottom = "0";
  cont.style.right = "0";
  cont.style.marginRight = "5px";
  cont.style.marginBottom = "5px";
  body.insertBefore(EditGlyph(id), body.firstChild);
  cont.appendChild(YesGlyph(id));
  cont.appendChild(NoGlyph(id));
  body.appendChild(cont);
  return body;
};

function CheckNote(nameId, contentId) {
  if (document.getElementById(nameId).value == "" || document.getElementById(contentId).value == "")
    return false;
  return true;
};