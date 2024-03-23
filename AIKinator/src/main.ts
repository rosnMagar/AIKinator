import './index.css'

const App = () => {
  const optionListUL:HTMLUListElement | null= document.getElementById("options") as HTMLUListElement;
  const options = ['Yes', 'No', 'A little', 'Very Much']
  
  options.map((optionText:string) => {

    const option = document.createElement('li');
    option.className = "my-2";

    const optionButton = document.createElement('button');
    optionButton.className = "bg-blue-500 justify-center w-full bg-blue-500 hover:bg-blue-400 text-white font-bold py-2 px-4"
    optionButton.textContent = optionText;
    option.appendChild(optionButton);

    optionListUL?.appendChild(option)

  });
}
App();
