<script>
import '@fullcalendar/core/vdom';
import FullCalendar from '@fullcalendar/vue';
import dayGridPlugin from '@fullcalendar/daygrid';
import interactionPlugin from '@fullcalendar/interaction';

export default {
  props: {
    deadline: Array,
  },
  components: {
    FullCalendar, // make the <FullCalendar> tag available
  },
  data() {
    return {
      calendarOptions: {
        plugins: [dayGridPlugin, interactionPlugin],
        initialView: 'dayGridMonth',
        defaultTimedEventDuration: '00:00',
        events: [],
      },
    };
  },
  methods: {
    onClick() {
      const cal = this.deadline.map(({ name: title, time: start }) => ({ title, start }));
      // console.log(JSON.stringify(cal));
      this.calendarOptions.events = cal;
    },
  },
  async mounted() {
    const cal = this.deadline.map(({ name: title, time: start }) => ({ title, start }));
    console.log(JSON.stringify(cal));
    this.calendarOptions.events = cal;
  },
};
</script>

<template>
  <div>
  <button type="button" class="btn btn-success btn-sm" @click="onClick">Refresh</button>
  <br><br>
  <FullCalendar :options="calendarOptions" />
  </div>
</template>
