Page({
  data: {
    // 状态选项卡
    statusTabs: [
      { text: '全部', status: 'all', count: 12 },
      { text: '待确认', status: 'pending', count: 3 },
      { text: '已确认', status: 'confirmed', count: 4 },
      { text: '已完成', status: 'completed', count: 5 },
      { text: '已取消', status: 'canceled', count: 0 }
    ],
    currentTab: 0,
    viewMode: 'list',
    
    // 日历数据
    currentYear: new Date().getFullYear(),
    currentMonth: new Date().getMonth() + 1,
    weekDays: ['日', '一', '二', '三', '四', '五', '六'],
    calendarDays: [],
    selectedDay: null,
    selectedDayText: '',
    
    // 预约数据
    allAppointments: [
      {
        id: 'a001',
        date: '2024-04-21',
        timeSlot: '09:00-10:00',
        clientName: '张女士',
        serviceType: '个人咨询',
        status: 'pending',
        statusText: '待确认',
        note: '第一次咨询，有些紧张',
        dayText: '周日',
        dateText: '4月21日'
      },
      {
        id: 'a002',
        date: '2024-04-21',
        timeSlot: '11:00-12:00',
        clientName: '李先生',
        serviceType: '焦虑管理',
        status: 'confirmed',
        statusText: '已确认',
        note: '',
        dayText: '周日',
        dateText: '4月21日'
      },
      {
        id: 'a003',
        date: '2024-04-22',
        timeSlot: '14:00-15:00',
        clientName: '王先生',
        serviceType: '抑郁症治疗',
        status: 'completed',
        statusText: '已完成',
        note: '继续上次的治疗方案',
        dayText: '周一',
        dateText: '4月22日'
      }
    ],
    currentAppointments: []
  },

  onLoad() {
    this.initCalendar();
    this.filterAppointments();
  },

  // 切换标签页
  switchTab(e) {
    const index = e.currentTarget.dataset.index;
    this.setData({
      currentTab: index
    });
    this.filterAppointments();
  },

  // 切换视图模式
  switchView(e) {
    const mode = e.currentTarget.dataset.mode;
    this.setData({
      viewMode: mode
    });
    if (mode === 'calendar') {
      this.initCalendar();
    }
  },

  // 筛选预约列表
  filterAppointments() {
    const status = this.data.statusTabs[this.data.currentTab].status;
    let appointments = this.data.allAppointments;
    if (status !== 'all') {
      appointments = appointments.filter(app => app.status === status);
    }
    this.setData({
      currentAppointments: appointments
    });
  },

  // 确认预约
  async confirmAppointment(e) {
    const id = e.currentTarget.dataset.id;
    wx.showModal({
      title: '确认预约',
      content: '确定要接受此预约吗？',
      success: async (res) => {
        if (res.confirm) {
          try {
            // TODO: Replace with actual API call
            await wx.cloud.callFunction({
              name: 'confirmAppointment',
              data: { id }
            });
            wx.showToast({
              title: '已确认预约',
              icon: 'success'
            });
            this.updateAppointmentStatus(id, 'confirmed', '已确认');
          } catch (error) {
            console.error('确认预约失败:', error);
            wx.showToast({
              title: '操作失败',
              icon: 'none'
            });
          }
        }
      }
    });
  },

  // 婉拒预约
  rejectAppointment(e) {
    const id = e.currentTarget.dataset.id;
    wx.showModal({
      title: '婉拒预约',
      content: '确定要婉拒此预约吗？',
      success: async (res) => {
        if (res.confirm) {
          try {
            // TODO: Replace with actual API call
            await wx.cloud.callFunction({
              name: 'rejectAppointment',
              data: { id }
            });
            wx.showToast({
              title: '已婉拒预约',
              icon: 'success'
            });
            this.updateAppointmentStatus(id, 'canceled', '已取消');
          } catch (error) {
            console.error('婉拒预约失败:', error);
            wx.showToast({
              title: '操作失败',
              icon: 'none'
            });
          }
        }
      }
    });
  },

  // 完成预约
  completeAppointment(e) {
    const id = e.currentTarget.dataset.id;
    wx.showModal({
      title: '完成预约',
      content: '确定要标记此预约为已完成吗？',
      success: async (res) => {
        if (res.confirm) {
          try {
            // TODO: Replace with actual API call
            await wx.cloud.callFunction({
              name: 'completeAppointment',
              data: { id }
            });
            wx.showToast({
              title: '预约已完成',
              icon: 'success'
            });
            this.updateAppointmentStatus(id, 'completed', '已完成');
          } catch (error) {
            console.error('完成预约失败:', error);
            wx.showToast({
              title: '操作失败',
              icon: 'none'
            });
          }
        }
      }
    });
  },

  // 改期预约
  rescheduleAppointment(e) {
    const id = e.currentTarget.dataset.id;
    wx.navigateTo({
      url: `/pages/counselor/appointments/reschedule?id=${id}`
    });
  },

  // 查看预约详情
  viewAppointmentDetail(e) {
    const id = e.currentTarget.dataset.id;
    wx.navigateTo({
      url: `/pages/counselor/appointments/detail?id=${id}`
    });
  },

  // 更新预约状态
  updateAppointmentStatus(id, status, statusText) {
    const { allAppointments } = this.data;
    const index = allAppointments.findIndex(app => app.id === id);
    if (index > -1) {
      allAppointments[index].status = status;
      allAppointments[index].statusText = statusText;
      this.setData({ allAppointments });
      this.filterAppointments();
      this.initCalendar();
    }
  },

  // 初始化日历
  initCalendar() {
    const today = new Date();
    const year = this.data.currentYear;
    const month = this.data.currentMonth - 1; // JavaScript月份从0开始
    
    // 获取月份的第一天和最后一天
    const firstDay = new Date(year, month, 1);
    const lastDay = new Date(year, month + 1, 0);
    
    // 当月天数
    const daysInMonth = lastDay.getDate();
    
    // 第一天是星期几（0是星期日）
    const firstDayOfWeek = firstDay.getDay();
    
    // 日历中可能显示上个月的最后几天
    const daysFromPrevMonth = firstDayOfWeek;
    
    // 获取上个月的最后几天
    const prevMonth = new Date(year, month, 0);
    const prevMonthDays = prevMonth.getDate();
    
    // 生成日历数组
    const calendarDays = [];
    
    // 添加上个月的天数
    for (let i = prevMonthDays - daysFromPrevMonth + 1; i <= prevMonthDays; i++) {
      const dayDate = new Date(year, month - 1, i);
      calendarDays.push({
        day: i,
        date: dayDate,
        isCurrentMonth: false,
        isToday: false,
        appointments: this.getAppointmentsForDate(dayDate)
      });
    }
    
    // 添加当月的天数
    for (let i = 1; i <= daysInMonth; i++) {
      const dayDate = new Date(year, month, i);
      const isToday = 
        dayDate.getDate() === today.getDate() && 
        dayDate.getMonth() === today.getMonth() && 
        dayDate.getFullYear() === today.getFullYear();
      
      const dayData = {
        day: i,
        date: dayDate,
        isCurrentMonth: true,
        isToday: isToday,
        appointments: this.getAppointmentsForDate(dayDate)
      };
      
      calendarDays.push(dayData);
      
      // 如果是今天，默认选中
      if (isToday) {
        this.setData({
          selectedDay: dayData,
          selectedDayText: this.formatSelectedDay(dayData)
        });
      }
    }
    
    // 添加下个月的开始几天，使日历填满6行
    const totalDaysNeeded = 42; // 6行 x 7天
    const nextMonthDays = totalDaysNeeded - calendarDays.length;
    
    for (let i = 1; i <= nextMonthDays; i++) {
      const dayDate = new Date(year, month + 1, i);
      calendarDays.push({
        day: i,
        date: dayDate,
        isCurrentMonth: false,
        isToday: false,
        appointments: this.getAppointmentsForDate(dayDate)
      });
    }
    
    this.setData({ calendarDays });
  },

  // 获取指定日期的预约
  getAppointmentsForDate(date) {
    const dateString = this.formatDate(date);
    return this.data.allAppointments.filter(app => app.date === dateString);
  },

  // 选择日期
  selectDay(e) {
    const day = e.currentTarget.dataset.day;
    this.setData({
      selectedDay: day,
      selectedDayText: this.formatSelectedDay(day)
    });
  },

  // 切换月份
  changeMonth(e) {
    const offset = parseInt(e.currentTarget.dataset.offset);
    let year = this.data.currentYear;
    let month = this.data.currentMonth + offset;
    
    if (month > 12) {
      month = 1;
      year++;
    } else if (month < 1) {
      month = 12;
      year--;
    }
    
    this.setData({
      currentYear: year,
      currentMonth: month
    });
    this.initCalendar();
  },

  // 格式化日期为YYYY-MM-DD
  formatDate(date) {
    const year = date.getFullYear();
    const month = (date.getMonth() + 1).toString().padStart(2, '0');
    const day = date.getDate().toString().padStart(2, '0');
    return `${year}-${month}-${day}`;
  },

  // 格式化选中日期显示
  formatSelectedDay(day) {
    const date = day.date;
    const month = date.getMonth() + 1;
    const dayNum = date.getDate();
    const weekDays = ['周日', '周一', '周二', '周三', '周四', '周五', '周六'];
    const weekDay = weekDays[date.getDay()];
    
    return `${month}月${dayNum}日 ${weekDay}`;
  }
}); 