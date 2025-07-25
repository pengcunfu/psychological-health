// useTheme.js - 用于获取主题变量的组合式钩子函数

import { reactive } from 'vue';

/**
 * 返回主题相关的颜色变量和样式
 * @returns {Object} 主题变量对象
 */
export function useTheme() {
  // 主题变量，与theme.scss保持一致
  const theme = reactive({
    // 主色调
    mgPrimary: '#E2AA59',
    mgPrimaryLight: '#F0D3A3',
    mgPrimaryDark: '#C29048',
    mgAccent: '#E15B64',
    mgAccentLight: '#F19299',
    mgAccentDark: '#B73C43',

    // 文本颜色
    mgTextPrimary: '#333333',
    mgTextSecondary: '#666666',
    mgTextTertiary: '#999999',
    mgTextLight: '#CCCCCC',

    // 背景色
    mgWhite: '#FFFFFF',
    mgBgPrimary: '#FFFFFF',
    mgBgSecondary: '#F5F5F5',
    mgGray100: '#F8F9FA',
    mgGray200: '#E9ECEF',
    
    // 边框色
    mgBorderLight: '#EEEEEE',
    mgBorderStandard: '#DDDDDD',
    
    // 中性色
    mgBlack: '#000000',
    mgGray400: '#CCCCCC',
    mgGray500: '#AAAAAA',
    mgGray800: '#343A40',
    
    // 功能色
    mgSuccess: '#52C41A',
    mgWarning: '#FAAD14',
    mgError: '#F5222D',
    mgInfo: '#1890FF',
    
    // 阴影
    mgShadowLight: '0 2px 8px rgba(0, 0, 0, 0.05)',
    mgShadowMedium: '0 4px 16px rgba(0, 0, 0, 0.1)',
    mgShadowDark: '0 8px 24px rgba(0, 0, 0, 0.15)',
  });

  return theme;
} 