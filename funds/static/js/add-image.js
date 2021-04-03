let birdForm = document.querySelectorAll(".bird-form")
let container = document.querySelector("#form-container")
let addButton = document.querySelector("#add-form")
let totalForms = document.querySelector("#id_form-TOTAL_FORMS")

let formNum = birdForm.length - 1
addButton.addEventListener('click', addForm)

function addForm(e) {
    e.preventDefault()

    let newForm = birdForm[0].cloneNode(true)
    let formRegex = RegExp(`form-(\\d){1}-`, 'g')

    formNum++
    newForm.innerHTML = newForm.innerHTML.replace(formRegex, `form-${formNum}-`)
    container.insertBefore(newForm, addButton)

    totalForms.setAttribute('value', `${formNum+1}`)
    console.log(formNum);
    console.log("{{ formset.max_num }}");

    if (formNum > (Number("{{ formset.max_num }}") - 2)) {
        addButton.style.display = "none"
    }
}