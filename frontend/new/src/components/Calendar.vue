<script>
import '@fullcalendar/core/vdom';
import FullCalendar from '@fullcalendar/vue';
import dayGridPlugin from '@fullcalendar/daygrid';
import interactionPlugin from '@fullcalendar/interaction';
import { isMobile } from 'mobile-device-detect';

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
    // fill the calendar with events
    refresh(deadline) {
      const cal = deadline.map(({ id, name: title, time: start }) => ({ id, title, start }));
      this.calendarOptions.events = cal;
    },
    // handle click on the calendar (interactive)
    handleEventClick(event) {
      this.$parent.$bvModal.show('update-modal');
      this.$parent.editDeadline(event.event.id);
    },
  },
  created() {
    // change view for mobile device
    if (isMobile) {
      this.calendarOptions.initialView = 'dayGridDay';
    }
  },
};
</script>

<template>
  <div>
  <FullCalendar :options="calendarOptions" />
  </div>
</template>
