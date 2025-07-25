import userApi from './user';
import counselorApi from './counselor';
import courseApi from './course';
import appointmentApi from './appointment';
import favoriteApi from './favorite';
import commonApi from './common';

export const user = userApi;
export const counselor = counselorApi;
export const course = courseApi;
export const appointment = appointmentApi;
export const favorite = favoriteApi;
export const common = commonApi;

export default {
  user,
  counselor,
  course,
  appointment,
  favorite,
  common
};
