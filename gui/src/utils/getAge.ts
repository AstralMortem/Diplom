export function getAge(date: string | undefined) {
    if(!date) return ''
    const currentYear = new Date().getFullYear()
    const year = new Date(date).getFullYear()
    const age = currentYear - year
    
    if(age.toString().endsWith('1')){
        return `${age} рік`
    }else if(age.toString().endsWith('2') || age.toString().endsWith('3') || age.toString().endsWith('4')){
        return `${age} роки`
    }else{
        return `${age} років`
    }
    
}
