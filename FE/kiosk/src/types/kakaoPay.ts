import { CartItem } from './order';

export interface PayRequest {
  itemName: string;
  totalAmount: number;
  sessionId: string;
}

export interface Pay {
  tid: string;
  next_redirect_pc_url: string;
  next_redirect_mobile_url: string;
  next_redirect_app_url: string;
}

export interface PaySuccessRequest {
  orderId: string;
  pgToken: string;
  cart: CartItem[];
}

export interface PaySuccess {
  aid: string;
  tid: string;
  cid: string;
  partner_order_id: string;
  partner_user_id: string;
  payment_method_type: string;
  item_name: string;
  item_code: string;
  quantity: number;
  created_at: string;
  approved_at: string;
  payload: string;
}
