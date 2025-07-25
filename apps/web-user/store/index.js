import { defineStore } from 'pinia';
import { useUserStore } from './user';

export const useCounterStore = defineStore('counter', {
	state: () => {
		return { count: 0 };
	},
	actions: {
		increment() {
			this.count++;
		},
	},
});

export { useUserStore };
