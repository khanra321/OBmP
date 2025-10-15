let nameError = document.getElementById("name-error");
let passwordError = document.getElementById("password-error");
let submitError = document.getElementById("log-error");

let main_body = document.getElementById("main");
// main_body.style.display = "none";


function validateName(){
    let name = document.getElementById("user_in").value;
    if(name.length == 0){
        nameError.innerHTML = 'Name is required';
        return false;
    }
    // if(name != "Akash Khanra"){
    //     nameError.innerHTML = 'write proper name'; 
    //     return false;
    // }
    else{
    nameError.innerHTML = 'valid';
    return true;
    }

}

function validatePassword(){
    let password = document.getElementById("pass_in").value;
    if(password.length == 0){
        passwordError.innerHTML = 'password is required';
        return false;
    // }
    // if(password != "#@Kash%321"){
    //     passwordError.innerHTML = ' write proper password ';
    //     return false;
    }else{
        passwordError.innerHTML = 'valid';
    return true;
    }

}

function validateForm(){

    let log_boxs = document.getElementById("log_box");
    
    if(!validateName() || !validatePassword()){
        submitError.innerHTML = "Please fix error";
        return false;
    }else{
        log_boxs.style.display = "none";
        main_body.style.display = "block";
    }
}



//deposit
document.getElementById("deposit-btn").addEventListener("click",deposit_fn);

function deposit_fn(){
    let input_amount = parseFloat(document.getElementById("input-deposit").value);
    // let deposit_number =parseFloat(document.getElementById("deposit-number").innerHTML);

    // let total = deposit_number + input_amount;
    document.getElementById("deposit-number").innerHTML = input_amount;
    //deposit
    let depoam = parseFloat(document.getElementById("depo-am").innerHTML);

    let total_depo = input_amount;

    document.getElementById("depo-am").innerHTML = total_depo;

    //blance
    let blance = parseFloat(document.getElementById("blance").innerHTML);
    let total_blance = blance + input_amount;
    document.getElementById("blance").innerHTML = total_blance;
}


//widthdraw

document.getElementById("withdraw-btn").addEventListener("click", withdrawfn);

function withdrawfn(){
    let with_input = parseFloat(document.getElementById("with-input").value);
    
    // let with_amount = parseFloat(document.getElementById("with-amount").innerHTML);

    // let total_with = with_input + with_amount;
    document.getElementById("with-amount").innerHTML = with_input;

    // widthdraw

    let wit = parseFloat(document.getElementById("wit-am").innerHTML);
    let totalwi = wit + with_input;
    document.getElementById("wit-am").innerHTML = totalwi;

    // blance
    let totalbl = document.getElementById("blance").innerHTML;
    let mainbl = totalbl - with_input;

    document.getElementById("blance").innerHTML = mainbl;


}
