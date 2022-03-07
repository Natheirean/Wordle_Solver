function clear_fields() {
    document.getElementById("wordle-grid").value = "";
    document.getElementById("wordle-grid2").value = "";
    document.getElementById("wordle-grid3").value = "";
}

var input_dict = {};

// when the Submit Button is clicked, it should collect all the following:
// all the letter L1 to L5
// the 'color' code of those positions
function submitButtonClick() {

    // get all the letter L1 - L5 and store them in variables
    var inputL1 = document.getElementById('L1-input').value;
    var inputL2 = document.getElementById('L2-input').value;
    var inputL3 = document.getElementById('L3-input').value;
    var inputL4 = document.getElementById('L4-input').value;
    var inputL5 = document.getElementById('L5-input').value;

    // get the color/correctness of the letter
    // position 1
    var radioInput = document.getElementsByName('letter_position_1');
    for (i = 0; i < radioInput.length; i++) {
        if (radioInput[i].checked) {
            var colorL1 = radioInput[i].value;
        }
    };
    // position 2
    var radioInput = document.getElementsByName('letter_position_2');
    for (i = 0; i < radioInput.length; i++) {
        if (radioInput[i].checked) {
            var colorL2 = radioInput[i].value;
        }
    };
    // position 3
    var radioInput = document.getElementsByName('letter_position_3');
    for (i = 0; i < radioInput.length; i++) {
        if (radioInput[i].checked) {
            var colorL3 = radioInput[i].value;
        }
    };
    // position 4
    var radioInput = document.getElementsByName('letter_position_4');
    for (i = 0; i < radioInput.length; i++) {
        if (radioInput[i].checked) {
            var colorL4 = radioInput[i].value;
        }
    };
    // position 5
    var radioInput = document.getElementsByName('letter_position_5');
    for (i = 0; i < radioInput.length; i++) {
        if (radioInput[i].checked) {
            var colorL5 = radioInput[i].value;
        }
    };

    input_dict = {
        0: [colorL1, inputL1, "L1"],
        1: [colorL2, inputL2, "L2"],
        2: [colorL3, inputL3, "L3"],
        3: [colorL4, inputL4, "L4"],
        4: [colorL5, inputL5, "L5"]
    };

    const s = JSON.stringify(input_dict);
    $.ajax({
        url: "/guess",
        type: "POST",
        contentType: "application/json",
        data: JSON.stringify(s)
    });

};

