import userApi from './user';
import authApi from './auth';
import counselorApi from './counselor';
import reviewApi from './review';
import courseApi from './course';
import appointmentApi from './appointment';
import paymentApi from './payment';
import favoriteApi from './favorite';
import announcementApi from './announcement';
import fileApi from './file';
import commonApi from './common';

// 从各个模块中提取 API 类
const {
  UserApi
} = userApi;
const {
  AuthApi
} = authApi;
const {
  CounselorApi
} = counselorApi;
const {
  ReviewApi
} = reviewApi;
const {
  CourseApi,
  CourseReviewApi
} = courseApi;
const {
  AppointmentApi
} = appointmentApi;
const {
  PaymentApi
} = paymentApi;
const {
  FavoriteApi
} = favoriteApi;
const {
  AnnouncementApi
} = announcementApi;
const {
  FileApi
} = fileApi;
const {
  CommonApi
} = commonApi;

// 导出类
export {
  UserApi,
  AuthApi,
  CounselorApi,
  ReviewApi,
  CourseApi,
  CourseReviewApi,
  AppointmentApi,
  PaymentApi,
  FavoriteApi,
  AnnouncementApi,
  FileApi,
  CommonApi
};

// 默认导出
export default {
  // 类形式
  UserApi,
  AuthApi,
  CounselorApi,
  ReviewApi,
  CourseApi,
  CourseReviewApi,
  AppointmentApi,
  PaymentApi,
  FavoriteApi,
  AnnouncementApi,
  FileApi,
  CommonApi,
};