async function PredictPurity() {
  // Define an async function that delays output
  let waterImage = document.querySelector(".test-water-image");
  async function delayedOutput() {
    const delay = (ms) => new Promise((resolve) => setTimeout(resolve, ms));
    console.log("Waiting for 5 seconds...");
    waterImage.src = "load.gif";
    await delay(5000);
    console.log("5 seconds have passed!");
    let randomValue = Math.random();
    result = randomValue <= 0.5 ? 0 : 1;
    return result;
  }

  // Call the async function and await its result
  const randomNumber = await delayedOutput(); // Await the result here

  // Wait for the async operation to complete
  if (randomNumber == 1) {
    waterImage.src = "drop.gif"; // Update the image source
  } else if (randomNumber == 0) {
    waterImage.src = "pollution.gif"; // Update the image source
  }
}

let button = document.getElementById('submitButton');
button.addEventListener('click', () => {
  PredictPurity();
});

// let addFile=document.getElementById('addFile');
// addFile.addEventListener('click',()=>{
  
// })
