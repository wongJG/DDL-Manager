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
    FullCalendar,
  },
  data() {
    return {
      calendarOptions: {
        plugins: [dayGridPlugin, interactionPlugin],
        initialView: 'dayGridMonth',
        defaultTimedEventDuration: '00:00',
        events: [],
        eventClick: this.handleEventClick,
      },
    };
  },
  methods: {
    refresh(deadline) {
      const cal = deadline.map(({ id, name: title, time: start }) => ({ id, title, start }));
      this.calendarOptions.events = cal;
    },
    handleEventClick(event) {
      // console.log(event.event.id);
      this.$parent.$bvModal.show('update-modal');
      this.$parent.editDeadline(event.event.id);
    },
  },
};
</script>

<template>
  <div>
  <FullCalendar :options="calendarOptions" />
  </div>
</template>
