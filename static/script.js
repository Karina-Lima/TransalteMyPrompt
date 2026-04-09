const input = document.getElementById("prompt-input");
const button = document.getElementById("optimize-btn");

const output = document.getElementById("optimized-output");
const scoreNumber = document.getElementById("score-number");
const scoreFill = document.getElementById("score-fill");
const strengthsList = document.getElementById("strengths-list");
const improvementsList = document.getElementById("improvements-list");
const copyBtn = document.getElementById("copy-btn");


button.addEventListener("click", optimizePrompt);


input.addEventListener("keydown", function(event){

    if(event.key === "Enter" && !event.shiftKey){
        event.preventDefault();
        optimizePrompt();
    }

});


async function optimizePrompt(){

    const prompt = input.value;

    if(!prompt.trim()) return;


    output.innerHTML = "Analisando...";


    try{

        const response = await fetch("/optimize", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ prompt })
        });


        if(!response.ok){
            throw new Error("Erro no servidor");
        }


        const data = await response.json();


        output.innerHTML = data.optimized_prompt;

        scoreNumber.innerHTML = `${data.score}/100`;

        scoreFill.style.width = `${data.score}%`;


        strengthsList.innerHTML = "";

        data.strengths.forEach(item=>{
            strengthsList.innerHTML += `<li>${item}</li>`;
        });


        improvementsList.innerHTML = "";

        data.improvements.forEach(item=>{
            improvementsList.innerHTML += `<li>${item}</li>`;
        });

    }

    catch(error){

        console.error(error);

        output.innerHTML = "Erro ao processar prompt.";

    }

}


// BOTÃO COPY FUNCTION 
copyBtn.addEventListener("click", async () => {

    const text = output.innerText;

    if(!text || text.trim() === "..." || text.includes("Analisando")) return;

    try {
        await navigator.clipboard.writeText(text);

        // feedback visual
        copyBtn.classList.add("copied");
        copyBtn.innerText = "✓";

        setTimeout(() => {
            copyBtn.classList.remove("copied");
            copyBtn.innerText = "📋";
        }, 1500);

    } catch (err) {
        console.error("Erro ao copiar:", err);
    }

});