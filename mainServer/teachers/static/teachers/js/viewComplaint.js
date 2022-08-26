function sortTable(n) {
    var table, rows, switching, i, x, y, shouldSwitch, dir, switchcount = 0;
    table = document.getElementById("table");
    switching = true;
    dir = "asc";
    while (switching) {
      switching = false;
      rows = table.rows;
      for (i = 1; i < (rows.length - 1); i++) {
        shouldSwitch = false;
        x = rows[i].getElementsByTagName("TD")[n].innerHTML.toLowerCase();
        y = rows[i + 1].getElementsByTagName("TD")[n].innerHTML.toLowerCase();

        if (!isNaN(parseInt(x))){
            x=parseInt(x)
            y=parseInt(y)
        }else{
            console.log(x,y)
        }
        if (dir == "asc") {
          if (x > y) {
            shouldSwitch = true;
            break;
          }
        } else if (dir == "desc") {
          if (x < y) {
            shouldSwitch = true;
            break;
          }
        }
      }
      if (shouldSwitch) {
        rows[i].parentNode.insertBefore(rows[i + 1], rows[i]);
        switching = true;
        switchcount ++;
      } else {
        if (switchcount == 0 && dir == "asc") {
          dir = "desc";
          switching = true;
        }
      }
    }
  }

let searchInp=document.getElementById("search")
let complaintIdSearch = document.getElementById("complaintId")

searchInp.addEventListener('change',e=>{
  let rows = document.getElementsByClassName("row")
  let searchText=searchInp.value
  console.log(searchText)
  for (row of rows){
    if (!row.innerText.includes(searchText)){
      row.classList.add("dNone")
    }else{
      row.classList.remove("dNone")
    }
  }
})

complaintIdSearch.addEventListener('change',e=>{
  let rows = document.getElementsByClassName("row")
  let searchText=complaintIdSearch.value
  console.log(searchText)
  for (row of rows){
    if (row.getElementsByTagName("td")[0].innerText==searchText){
      row.classList.remove("dNone")
    }else{
      row.classList.add("dNone")
    }
  }
})