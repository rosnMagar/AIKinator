import './index.css'

// we only use this for temporary purpose
const host = 'http://150.243.210.198:8000/'

var res:any = {
    "answer": -1,
    "question_id": 0
}

var predictionReached = false

const App = () => {
  const optionListUL:HTMLUListElement | null= document.getElementById("options") as HTMLUListElement;
  const questionText:HTMLElement = document.getElementById("question") as HTMLElement;
  const predictionText:HTMLElement = document.getElementById("prediction_text") as HTMLElement;
  const options = ['No', 'A Little', 'Yes', 'Very Much']

  // automatic reset
  var data = {
    "answer": -2,
    "question_id": 0
  }

  var option = {
    method: 'POST',
    // mode: 'no-cors',
    headers: {
      // "Access-Control-Allow-Origin": '*',
      // "Access-Control-Allow-Methods": '*', 
      // "Access-Control-Allow-Headers": 'Content-Type, Authorization',
      'Content-Type' : 'application/json',
    },
    body: JSON.stringify(data)
  } 
  
  fetch(`${host}`, option).then((data) => {
    return data.json()
  }).then((data) => {
    // res = data 
    // questionText.textContent = res.question
  })


  // get the first question
  data = {
    "answer": -1,
    "question_id": 0
  }

  option = {
    method: 'POST',
    // mode: 'no-cors',
    headers: {
      // "Access-Control-Allow-Origin": '*',
      // "Access-Control-Allow-Methods": '*', 
      // "Access-Control-Allow-Headers": 'Content-Type, Authorization',
      'Content-Type' : 'application/json',
    },
    body: JSON.stringify(data)
  } 
  
  fetch(`${host}`, option).then((data) => {
    return data.json()
  }).then((data) => {
    res = data 
    questionText.textContent = `Do you, or Have you Experienced from ${res.question.split("_").join(" ")}`
  })

  const setOnclickValue = (request_value:number) => {

    const data = {
      "answer": request_value,
      "question_id": res.question_id 
   }

    var option = {
      method: 'POST',
      // mode: 'no-cors',
      headers: {
        // "Access-Control-Allow-Origin": '*',
        // "Access-Control-Allow-Methods": '*', 
        // "Access-Control-Allow-Headers": 'Content-Type, Authorization',
        'Content-Type' : 'application/json',
      },
      body: JSON.stringify(data)
    } 

    fetch(`${host}`, option).then((data) => {
      return data.json()
    }).then((data) => {
      // res = data  
    })

    // 2nd api call
    data.answer = -1;
    // data.question_id = res.question_id

    option = {
      method: 'POST',
      // mode: 'no-cors',
      headers: {
        // "Access-Control-Allow-Origin": '*',
        // "Access-Control-Allow-Methods": '*', 
        // "Access-Control-Allow-Headers": 'Content-Type, Authorization',
        'Content-Type' : 'application/json',
      },
      body: JSON.stringify(data)
    } 

    fetch(`${host}`, option).then((data) => {
      return data.json()
    }).then((data) => {
      res = data  
      if(data.type == "question")
        questionText.textContent = `Do you, or Have you Experienced from ${(res.question.split("_").join(' '))}`
      else
        predictionReached = true;
        res.value.map((key) => {
          const li = document.createElement('li') 
          li.textContent = Object.keys(key)[0] +" : " + (key[Object.keys(key)[0]] * 100).toFixed(2) + " %" 
          console.log(key)
          predictionText.appendChild(li)
        })
      })

  }
  options.map((optionText:string, i: number) => {

    const option = document.createElement('li');
    option.className = "my-2";

    const optionButton = document.createElement('button');
    optionButton.className = "bg-blue-500 justify-center w-72 bg-blue-500 hover:bg-blue-400 text-white font-bold py-2 px-4"
    optionButton.textContent = optionText;
    option.appendChild(optionButton);

    option.onclick = () => setOnclickValue(i * (0.33));
    optionListUL?.appendChild(option)
  });

  
}
App();
