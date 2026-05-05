/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */

import { Product, NewsItem, AccessoryCategory } from './types';

export const PRODUCTS: Product[] = [
  {
    id: 'p1',
    name: 'iPhone 15 Pro 128GB Chính hãng VN/A',
    price: 24590000,
    originalPrice: 28990000,
    image: 'https://lh3.googleusercontent.com/aida-public/AB6AXuDnzjcynjdAUiQkcaEyA39jLDSNseZ0uL4SX1vdfbAejlPeCyZrnFXNFDKjRx13Ot9HXk71d4E_vainL3sCg3H561qGyGeJsWo3YVWtb0ZUPUg0pWI92RO-_Yd4766bYnfOipOCXQMflk9fBcGTRigyU934_njgV6Tq6l5xp7cfWYPuZcDDTWBfOUgP5snvyvnMkjUjy872aBseF3Lon6W-s_4JMatj9eXTvZm6D4RrlfcopF8ptcmPGhSZz3uXxj8_-MqG6wkU-_c',
    category: 'Smartphones',
    brand: 'Apple',
    rating: 5,
    reviewsCount: 42,
    badges: ['-15%', 'Trả góp 0%'],
  },
  {
    id: 'p2',
    name: 'Samsung Galaxy S24 Ultra 256GB',
    price: 28490000,
    originalPrice: 33990000,
    image: 'https://lh3.googleusercontent.com/aida-public/AB6AXuCWGlM6_Feqw8X18KJt44y7o37CLBtsDxxIqBgWNWdC5ZqtAEqLJZxQwMnGrOSWquibbdcoLNQA_1AiqtZNt03thVfexSQhzXeqCpYqZnE3PoLXyV5HPjqHSOijV7_Tdx__76v9iNPNTcyfYiCArxeE2ykJniHMqcppO9FIrZrggEvrdjo8WQwiV1QkJiQZ8TMUJtrtQuOaI4DwqHQ0WD6wFxCJ-Sx1QDJqe2e2alI_lUowjlDqsRKbhd1ntKG6eQEn63yIkMQ9dLk',
    category: 'Smartphones',
    brand: 'Samsung',
    rating: 5,
    reviewsCount: 128,
    badges: ['-10%', 'Trả góp 0%'],
  },
  {
    id: 'p3',
    name: 'Xiaomi 14 Ultra 16GB/512GB Leica',
    price: 26990000,
    originalPrice: 32990000,
    image: 'https://lh3.googleusercontent.com/aida-public/AB6AXuCkuEDfZk4yTJSbrMYQZyPTxtAVEAtSmb-Mgo72ZUAmHKstjOj_yUaYV5pi8WjdST-0FCLwPVkVyerJLtj96RQd-iYkyZ5YBVEkg6apWhkfizu7cmj28mTiRRLTCbLIFl2qU5iBabdaSxPFHr7RkoNvoH5tchsoyE28JglGk5DiFYanG5w3s0gf8_r27SiVMf5hw9JCr3uWonxMMiWl5imU_eaQXKqubE-yVVUzu3dOGur4vHTa48c869hfH8Wm13fNTljD-N6UAak',
    category: 'Smartphones',
    brand: 'Xiaomi',
    rating: 4,
    reviewsCount: 15,
    badges: ['-22%'],
  },
  {
    id: 'p4',
    name: 'Apple Watch Series 9 GPS 41mm',
    price: 9490000,
    originalPrice: 10990000,
    image: 'https://lh3.googleusercontent.com/aida-public/AB6AXuD_4zRl_rMusIA8gQNom0dd3sxTR3fNv4pYtNPOt99-kHwNNDGYslYHxjWbrQ7RUfg9JHWNnGKZvac8HAgPCF2Bcyq8Z0eANpdzld5dXUpYkkG_YCiIf72JrPpd12agQY0GYm15HIJBJBzgXEoAtlKXGIYFP3qXhgO-KFk-WZS_Q0o89tnt9T7sWX07Qhcx_v-m_UOdu68HNT2mSgPCf5kT23rAYWFcnHHwAxlcM03XFdIiOV76011i-v6eqGVcg3seSaraQkzBwlI',
    category: 'Smartwatches',
    brand: 'Apple',
    rating: 5,
    reviewsCount: 89,
    badges: ['Trả góp 0%'],
  },
  {
    id: 'p5',
    name: 'Oppo Reno11 Pro 5G 12GB/512GB',
    price: 15490000,
    originalPrice: 16990000,
    image: 'https://lh3.googleusercontent.com/aida-public/AB6AXuBd4WtOOq6sbURoQ8qYwZu1NvwFCOxuqsMQUIlx9dLsYB2yF8c2aSi6n3eKweAWg7uhmRSixmjjrIh5N1uhEYsdtWDE4pfIOrrRRZZHuqY3U7cutGoboHq468V-Cmy1yUedCMp2Mtzjd59jFjhbeegpz42kla0n-RvOXlwX7BmLXci07x05PASHb_tjZOvrhgk39K976QeMw9xzCFLaKEqIkP47t-YeZLHfh_T-X4Gl7gXLKbcAyBrDCsB1At1_6-M3d1qsFQVBweQ',
    category: 'Smartphones',
    brand: 'Oppo',
    rating: 4,
    reviewsCount: 32,
    badges: ['-5%'],
  },
  {
    id: 'probook-x1',
    name: 'ProBook Ultimate X1',
    price: 1999,
    originalPrice: 2499,
    image: 'https://lh3.googleusercontent.com/aida-public/AB6AXuACcOyCxVQ7Yev2SctYJwq8xfKLa9NGdxRmxJFWbms4L-KUJ378MRR_p1zegsxGObBMshnsQjyCB_Nhi9DGTTnVVnf3KitkAA3DTiJowBGjmDFYV93fVhXn-PtxikZR5g6B19arvNLfbPHp9XJKxMnhzapTjTk8PWNMItS6A6sAHSsHvM9qsPOsqP2NaXLjuEJZobvkwltLQWAEJz_E2HPzwovHq1ic4a3tDE1Gh5hvM2umJOUIIyuwUBvezLLZIlolA1gQSSaZlvA',
    category: 'Laptops',
    brand: 'WiseTech',
    rating: 4.9,
    reviewsCount: 128,
    badges: ['Sale'],
    specs: {
      'Processor': 'Octa-Core M3 Ultra',
      'Display': '16.2" Liquid Retina XDR',
      'Battery': 'Up to 22 Hours',
      'Unified Memory': '32GB LPDDR5X'
    },
    description: 'The ProBook Ultimate X1 represents the pinnacle of modern engineering, designed for professionals who refuse to compromise. Every element, from the precision-milled aerospace-grade aluminum chassis to the revolutionary cooling architecture, has been refined for peak performance and enduring style.',
    features: [
      'Advanced thermal management system for sustained high-performance workloads.',
      'Six-speaker sound system with force-cancelling woofers and spatial audio support.',
      'Sustainable design utilizing 100% recycled aluminum in the enclosure.'
    ],
    colors: ['#444748', '#dcdad6', '#fdd093'],
    storageOptions: ['512GB SSD', '1TB SSD', '2TB SSD']
  }
];

export const ACCESSORIES: AccessoryCategory[] = [
  { id: 'a1', name: 'Apple', icon: 'apple' },
  { id: 'a2', name: 'Sạc cáp', icon: 'charging_station' },
  { id: 'a3', name: 'Pin dự phòng', icon: 'battery_charging_full' },
  { id: 'a4', name: 'Tai nghe', icon: 'headphones' },
  { id: 'a5', name: 'Loa bluetooth', icon: 'speaker' },
  { id: 'a6', name: 'Thẻ nhớ', icon: 'sd_card' },
  { id: 'a7', name: 'Bàn phím', icon: 'keyboard' },
  { id: 'a8', name: 'Chuột', icon: 'mouse' },
  { id: 'a9', name: 'Bao da ốp lưng', icon: 'tablet_mac' },
  { id: 'a10', name: 'Dán màn hình', icon: 'screen_rotation' },
  { id: 'a11', name: 'Ổ cứng di động', icon: 'hard_drive' },
  { id: 'a12', name: 'Thiết bị mạng', icon: 'router' },
];

export const NEWS: NewsItem[] = [
  {
    id: 'n1',
    title: 'Đánh giá chi tiết iPhone 15 Pro Max sau 6 tháng sử dụng',
    excerpt: '1 giờ trước',
    date: '1 giờ trước',
    image: 'https://lh3.googleusercontent.com/aida-public/AB6AXuAlN3RY8Lf7Ubng4mhKbFdXQPgMdSvEzrKl6hd2oHNpcxUbXznjYAdvDABISVplUbPC2z_lE-p7QHTd3VUVAGqjNiGgO7A5Ot9P_pvoomKnhoMp61C0Ai2zru8_geT3vYYszj9plhWPVwwgfBcrNtcmyvFVMIbS6wDBBIZ0cQ51b8RJikL1H0d9E5E6DTMCI-EtWhohO2jCXtG43tIZGD61jdUElQXaTzEzsnMBA3wB44Q7hN6N7-1IfZk8L-E0VKMHO13iumDMV_U',
  },
  {
    id: 'n2',
    title: 'Samsung ra mắt bộ vi xử lý AI thế hệ mới cực mạnh',
    excerpt: '3 giờ trước',
    date: '3 giờ trước',
    image: 'https://lh3.googleusercontent.com/aida-public/AB6AXuCiQ4wE_p7ojg0QYkLsMngDT4XKXOtb4cHV-GDIqQEFVeK2_kx4zdp4d1DAU8M7HSjz8GpIvxSWnnfBIksCPB60YmHrGuaqawuP5cjnvipoU0AQ229LqIJLljHJHCSkddtfOckMYhxuWVFIRswPe_6CyHPLhHW76JXgKeOphXnLLEeuLVXJj_65q5PjfnndvYW14mJ3ofSaNOgZfqyTR0hFj5vS13mG6n0TR_YCo1OcBksE1i9iV8Pr3Tzg0AokoYBibFXE_OMoYtQ',
  },
  {
    id: 'n3',
    title: 'Top 5 laptop văn phòng đáng mua nhất tầm giá 20 triệu',
    excerpt: '5 giờ trước',
    date: '5 giờ trước',
    image: 'https://lh3.googleusercontent.com/aida-public/AB6AXuBji2cbxuIfyItlSfiEm9-kvSLIFkB2F7hg0yYffGgvAw3mjMPcLFQ75M03mjLhl-zosfnoV07-uIwdowwk6bH5SbjAtyjL8-tbxG8aNnaq__Lmr39ubGNUHm-JmdBQr0OyMP-LTkD1ndO59uIbLCMnZgcbFmXiwytJwJwbtan6De-vfWI2ojZ6NnyWsUxrtRBcblZvvTRarRqTo-lOgDHfweCtN9bDBa7wPfR3pEZyE3vP6tv0sZufBtxbO8-rEEWYfjj0FrhVrLg',
  },
];
