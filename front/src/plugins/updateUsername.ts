import { ref } from "vue";

const currentUser = ref('matias')
const currentUserId = ref(123)

export default function updateUsername() {

    function setCurrentUser(val: string, uid: number) {
        currentUser.value = val;
        currentUserId.value = uid;
    }

    return { currentUser, setCurrentUser, currentUserId }
}