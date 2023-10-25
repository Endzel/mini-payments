// Expected time: 30 mins
// Use jsfiddle.net (or your favorite text editor) to implement a function in JavaScript.
// The function should work for any valid input, don't worry about handling invalid inputs.
// (to be continued)
// Write a function that takes an Excel column name (A,B,C,D…AA,AB,AC,… AAA..) and returns a corresponding integer value (A=0,B=1,… AA=26...).
//
// I will try to finish it since it gave my pure curiosity, but for the moment, 1 hour into it I cannot go further since I need to leave now
// It was fun!
// I will probably for next steps, would try to look for a mathematical equation that will be returning the correct number since BA=52

/**
  * Returns specific value given a column name
  * @param columnName Characters of the column
*/

// Final solution achieved
function getValueFromColumn(columnName) {
  let result = 0;
  for (let i = 0; i < columnName.length; i++) {
    result += result * 25 + columnName.charCodeAt(i) - 65 + 1;
  }
  return result - 1;
}

console.log(getValueFromColumn("ZZZ"))
