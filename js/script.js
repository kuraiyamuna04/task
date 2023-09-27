function calculate(action){ 
    var val1 = document.getElementById("val1").value
    var val2 = document.getElementById("val2").value
   if (action=="add") 
   {
    document.getElementById("result").innerHTML = parseInt(val1) + parseInt(val2)
   }
   else if(action == "subtract")
   {
    document.getElementById("result").innerHTML = parseInt(val1) - parseInt(val2)
   }
   else if(action == "multiply")
   {
    document.getElementById("result").innerHTML = parseInt(val1) * parseInt(val2)
   }
   else if(action == "divide")
   {
    document.getElementById("result").innerHTML = parseInt(val1) / parseInt(val2)
   }
}