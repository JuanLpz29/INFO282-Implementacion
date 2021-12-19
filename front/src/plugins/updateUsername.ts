import { ref } from "vue";

const currentUser = ref('')
const currentUserId = ref(0)

export default function updateUsername() {

    function setCurrentUser(val: string, uid: number) {
        currentUser.value = val;
        currentUserId.value = uid;
    }

    return { currentUser, setCurrentUser, currentUserId }
}