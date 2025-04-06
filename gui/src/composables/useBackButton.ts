export const useBackButton = () => {
    const state = useState('backButton', () => false)
    return state
}
