/* eslint-disable */
<template>
  <q-page class="q-pa-sm">
      <b-navbar toggleable="lg" type="Dark" variant="Primary">
      <b-navbar-nav>

        <!-- navbar item -->
        <b-nav-item href="/project">Project</b-nav-item>
        <b-nav-item href="/deadline">Deadline</b-nav-item>
        <b-nav-item-dropdown>

        <!-- Dropdown item -->
          <template #button-content>
            <em>User</em>
          </template>
          <b-dropdown-item href="/settings">Profile</b-dropdown-item>
          <b-dropdown-item href="/signout">Sign Out</b-dropdown-item>
          <b-dropdown-item href="/admin">Admin</b-dropdown-item>
        </b-nav-item-dropdown>
      </b-navbar-nav>
  </b-navbar>
  <hr><br>
    
    <!-- Gantt graph -->
    <gantt-elastic
      :options="options"
      :tasks="tasks"
      @tasks-changed="tasksUpdate"
      @options-changed="optionsUpdate"
      @dynamic-style-changed="styleUpdate"
    >
      <gantt-header slot="header"></gantt-header>
    </gantt-elastic>


    <div class="q-mt-md" />
    <q-btn @click="addTask" icon="mdi-plus" label="Add task" />
  </q-page>
</template>

<style>
</style>

<script>
import GanttElastic from 'gantt-elastic';
import GanttHeader from 'gantt-elastic-header';
import dayjs from 'dayjs';

// get current dates
function getDate(hours) {
  const currentDate = new Date();
  const currentYear = currentDate.getFullYear();
  const currentMonth = currentDate.getMonth();
  const currentDay = currentDate.getDate();
  const timeStamp = new Date(
    currentYear,
    currentMonth,
    currentDay,
    0,
    0,
    0,
  ).getTime();
  return new Date(timeStamp + hours * 60 * 60 * 1000).getTime();
}
const tasks = [
  {
    id: 1,
    label: 'Make some noise',
    user:
      '<a href="mailto:liuche@gmail.com">Liu Che</a>',
    start: getDate(-24 * 5),
    duration: 15 * 24 * 60 * 60 * 1000,
    percent: 85,
    type: 'project',
  },
  {
    id: 2,
    label: 'With great power comes great responsibility',
    user:
      '<a href="mailto:wojian@gmail.com">Wang Wojian</a>',
    parentId: 1,
    start: getDate(-24 * 4),
    duration: 4 * 24 * 60 * 60 * 1000,
    percent: 50,
    type: 'milestone',
    collapsed: true,
    style: {
      base: {
        fill: '#1EBC61',
        stroke: '#0EAC51',
      },
    },
  },
  {
    id: 3,
    label: 'Courage is being scared to death, but saddling up anyway.',
    user:
      '<a href="https://www.google.com/search?q=John+Wayne" target="_blank" style="color:#0077c0;">John Wayne</a>',
    parentId: 2,
    start: getDate(-24 * 3),
    duration: 2 * 24 * 60 * 60 * 1000,
    percent: 100,
    type: 'task',
  },
  {
    id: 4,
    label: 'Put that toy AWAY!',
    user:
      '<a href="https://www.google.com/search?q=Clark+Kent" target="_blank" style="color:#0077c0;">Clark Kent</a>',
    start: getDate(-24 * 2),
    duration: 2 * 24 * 60 * 60 * 1000,
    percent: 50,
    type: 'task',
    dependentOn: [3],
  },
  {
    id: 5,
    label:
      'One billion, gajillion, fafillion... shabadylu...mil...shabady......uh, Yen.',
    user:
      '<a href="https://www.google.com/search?q=Austin+Powers" target="_blank" style="color:#0077c0;">Austin Powers</a>',
    parentId: 4,
    start: getDate(0),
    duration: 2 * 24 * 60 * 60 * 1000,
    percent: 10,
    type: 'milestone',
    style: {
      base: {
        fill: '#0287D0',
        stroke: '#0077C0',
      },
    },
  },
];
const options = {
  taskMapping: {
    progress: 'percent',
  },
  maxRows: 100,
  maxHeight: 500,
  title: {
    label: 'Your project title as html (link or whatever...)',
    html: false,
  },
  row: {
    height: 24,
  },
  calendar: {
    hour: {
      display: true,
    },
  },
  chart: {
    progress: {
      bar: false,
    },
    expander: {
      display: true,
    },
  },
  taskList: {
    expander: {
      straight: false,
    },
    columns: [
      {
        id: 1,
        label: 'ID',
        value: 'id',
        width: 40,
      },
      {
        id: 2,
        label: 'Description',
        value: 'label',
        width: 200,
        expander: true,
        html: true,
        events: {
          click({ data }) {
            alert(data.label);
          },
        },
      },
      {
        id: 3,
        label: 'Assigned to',
        value: 'user',
        width: 130,
        html: true,
      },
      {
        id: 3,
        label: 'Start',
        value: (task) => { dayjs(task.start).format('YYYY-MM-DD'); },
        width: 78,
      },
      {
        id: 4,
        label: 'Type',
        value: 'type',
        width: 68,
      },
      {
        id: 5,
        label: '%',
        value: 'progress',
        width: 35,
        style: {
          'task-list-header-label': {
            'text-align': 'center',
            width: '100%',
          },
          'task-list-item-value-container': {
            'text-align': 'center',
            width: '100%',
          },
        },
      },
    ],
  },
  locale: {
    name: 'en',
    Now: 'Now',
    'X-Scale': 'Zoom-X',
    'Y-Scale': 'Zoom-Y',
    'Task list width': 'Task list',
    'Before/After': 'Expand',
    'Display task list': 'Task list',
  },
};

export default {
  name: 'Gantt',
  components: {
    GanttElastic,
    GanttHeader,
  },
  data() {
    return {
      tasks,
      options,
      dynamicStyle: {},
      lastId: 16,
    };
  },
  methods: {
    addTask() {
      this.tasks.push({
        id: this.lastId + 1,
        label:
          '<a href="https://images.pexels.com/photos/423364/pexels-photo-423364.jpeg?auto=compress&cs=tinysrgb&h=650&w=940" target="_blank" style="color:#0077c0;">Yeaahh! you have added a task bro!</a>',
        user:
          '<a href="https://images.pexels.com/photos/423364/pexels-photo-423364.jpeg?auto=compress&cs=tinysrgb&h=650&w=940" target="_blank" style="color:#0077c0;">Awesome!</a>',
        start: getDate(24 * 3),
        duration: 1 * 24 * 60 * 60 * 1000,
        percent: 50,
        type: 'project',
      });
    },
    tasksUpdate(task) {
      this.tasks = task;
    },
    optionsUpdate(option) {
      this.options = option;
    },
    styleUpdate(style) {
      this.dynamicStyle = style;
    },
  },
};
</script>
