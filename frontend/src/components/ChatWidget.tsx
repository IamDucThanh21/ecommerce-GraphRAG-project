// import { useEffect, useState, useRef } from 'react';
// import { apiClient } from '../api/client';
// import { MessageSquare, X, Send, User, Bot } from 'lucide-react';
// import { motion, AnimatePresence } from 'motion/react';

// export default function ChatWidget() {
//   const [isAuthenticated, setIsAuthenticated] = useState(false);
//   const [isOpen, setIsOpen] = useState(false);
//   const [messages, setMessages] = useState([
//     { role: 'bot', content: 'Xin chào! Tôi có thể giúp gì cho bạn hôm nay?' }
//   ]);
//   const [input, setInput] = useState('');

//   const [conversationId, setConversationId] = useState<string | null>(null);
//   const [isSending, setIsSending] = useState(false);

//   const messagesEndRef = useRef<HTMLDivElement | null>(null);
//   const messagesContainerRef = useRef<HTMLDivElement | null>(null);

//   const handleSend = async () => {
//     const message = input.trim();

//     if (!message || isSending)
//       return;

//     setIsSending(true);

//     // show user message immediately
//     setMessages((prev) => [
//       ...prev,
//       {
//         role: 'user',
//         content: message,
//       },
//     ]);

//     setInput('');

//     try {
//       let currentConversationId =
//         conversationId;

//       /**
//        * First message:
//        * create conversation
//        */
//       if (!currentConversationId) {
//         const conversationResponse =
//           await apiClient.createConversation(
//             {
//               title: '',
//             }
//           );

//         currentConversationId =
//           conversationResponse.data[
//             'conversation-service-response'
//           ]._id;

//         if (!currentConversationId) {
//           throw new Error(
//             'Cannot create conversation'
//           );
//         }

//         setConversationId(
//           currentConversationId
//         );
//       }

//       /**
//        * Send message
//        */
//       const response =
//         await apiClient.sendMessage(
//           currentConversationId,
//           {
//             content: message,
//           }
//         );

//       const botMessage =
//         response.data[
//           'message-service-response'
//         ].bot_message.content;

//       if (botMessage) {
//         setMessages((prev) => [
//           ...prev,
//           {
//             role: 'bot',
//             content: botMessage,
//           },
//         ]);
//       }
//     } catch (error) {
//       console.error(
//         'Chat error:',
//         error
//       );

//       setMessages((prev) => [
//         ...prev,
//         {
//           role: 'bot',
//           content:
//             'Có lỗi xảy ra. Vui lòng thử lại.',
//         },
//       ]);
//     } finally {
//       setIsSending(false);
//     }
//   };

//   useEffect(() => {
//     const checkAuth = () => {
//       setIsAuthenticated(
//         apiClient.isAuthenticated()
//       );
//     };

//     checkAuth();

//     // update when localStorage changes
//     window.addEventListener('auth-change', checkAuth);

//     return () => {
//       window.removeEventListener(
//         'auth-change',
//         checkAuth
//       );
//     };
//   }, []);

//   useEffect(() => {
//     messagesEndRef.current?.scrollIntoView(
//       {
//         behavior: 'smooth',
//       }
//     );
//   }, [messages]);

//   if (!isAuthenticated) {
//     return null;
//   }

//   return (
//     <div className="fixed bottom-8 right-8 z-[1000]">
//       {/* Toggle Button */}
//       <button 
//         onClick={() => setIsOpen(!isOpen)}
//         className="w-16 h-16 bg-zinc-900 text-white rounded-full flex items-center justify-center shadow-2xl hover:scale-110 active:scale-95 transition-all group"
//       >
//         {isOpen ? <X className="w-6 h-6" /> : <MessageSquare className="w-6 h-6 group-hover:rotate-12 transition-transform" />}
//         {!isOpen && (
//           <span className="absolute -top-1 -right-1 w-5 h-5 bg-[#ba1a1a] rounded-full border-4 border-white"></span>
//         )}
//       </button>

//       {/* Chat Window */}
//       <AnimatePresence>
//         {isOpen && (
//           <motion.div 
//             initial={{ opacity: 0, y: 20, scale: 0.9 }}
//             animate={{ opacity: 1, y: 0, scale: 1 }}
//             exit={{ opacity: 0, y: 20, scale: 0.9 }}
//             className="absolute bottom-20 right-0 w-96 max-w-[calc(100vw-2rem)] bg-white rounded-[2.5rem] shadow-[0_20px_70px_-10px_rgba(0,0,0,0.2)] border border-zinc-100 overflow-hidden flex flex-col"
//           >
//             {/* Header */}
//             <div className="p-6 bg-zinc-900 text-white">
//               <div className="flex items-center gap-3">
//                 <div className="w-10 h-10 rounded-2xl bg-[#FFD194] flex items-center justify-center text-zinc-900">
//                   <Bot className="w-5 h-5" />
//                 </div>
//                 <div>
//                   <h3 className="font-black uppercase tracking-widest text-xs">WiseTech Assistant</h3>
//                   <div className="flex items-center gap-1.5 pt-0.5">
//                     <span className="w-1.5 h-1.5 bg-green-400 rounded-full animate-pulse"></span>
//                     <span className="text-[10px] font-bold text-zinc-400">Online now</span>
//                   </div>
//                 </div>
//               </div>
//             </div>

//             {/* Messages */}
//             <div className="flex-1 p-6 space-y-6 max-h-[400px] overflow-y-auto bg-zinc-50/50 scrollbar-hide">
//               {messages.map((msg, idx) => (
//                 <div
//                   key={idx}
//                   className={`flex ${
//                     msg.role === 'user'
//                       ? 'justify-end'
//                       : 'justify-start'
//                   }`}
//                 >
//                   <div
//                     className={`max-w-[80%] p-4 rounded-3xl text-sm font-medium ${
//                       msg.role === 'user'
//                         ? 'bg-zinc-900 text-white rounded-tr-none'
//                         : 'bg-white text-zinc-800 rounded-tl-none border border-zinc-100 shadow-sm'
//                     }`}
//                   >
//                     {msg.content}
//                   </div>
//                 </div>
//               ))}

//               <div ref={messagesEndRef} />
//             </div>

//             {/* Input */}
//             <div className="p-4 bg-white border-t border-zinc-100">
//               <div className="relative flex items-center">
//                 <input 
//                   type="text" 
//                   value={input}
//                   onChange={(e) => setInput(e.target.value)}
//                   onKeyDown={(e) => {
//                     if (e.key === 'Enter') {
//                       handleSend();
//                     }
//                   }}
//                   placeholder="Nhắn tin cho WiseTech..."
//                   className="w-full pl-6 pr-14 py-4 bg-zinc-100 rounded-2xl border-none outline-none font-medium text-xs focus:ring-2 focus:ring-zinc-900 transition-all"
//                 />
//                 <button 
//                   onClick={handleSend}
//                   disabled={isSending}
//                   className="absolute right-2 p-2 bg-zinc-900 text-white rounded-xl hover:bg-zinc-800 transition-all active:scale-90"
//                 >
//                   <Send className="w-4 h-4" />
//                 </button>
//               </div>
//             </div>
//           </motion.div>
//         )}
//       </AnimatePresence>
//     </div>
//   );
// }

import { useEffect, useState, useRef } from 'react';
import { apiClient } from '../api/client';
import { Page } from '../types';
import { MessageSquare, X, Send, Bot, ShoppingCart, ChevronRight } from 'lucide-react';
import { motion, AnimatePresence } from 'motion/react';

// ─── Constants ────────────────────────────────────────────────────────────────

const SMARTPHONE_CATEGORY_ID = '5e883863-9808-4319-acb7-078e6206798d';
const MAX_PRODUCT_CARDS = 3;

// ─── Types ────────────────────────────────────────────────────────────────────

interface ProductCard {
  product_id: string;
  name: string;
  price: number;
  image_url?: string;
}

interface Message {
  role: 'user' | 'bot';
  content: string;
  products?: ProductCard[];
  isLoadingProducts?: boolean;
}

interface ChatWidgetProps {
  setPage: (page: Page) => void;
  setProductId: (id: string) => void;
  setCategoryId: (id: string) => void;
}

// ─── Helpers ──────────────────────────────────────────────────────────────────

function formatVND(amount: number) {
  return amount.toLocaleString('vi-VN') + 'đ';
}

async function fetchProductCards(productIds: string[]): Promise<ProductCard[]> {
  const results = await Promise.allSettled(
    productIds.slice(0, MAX_PRODUCT_CARDS).map((id) =>
      apiClient.productDetail(SMARTPHONE_CATEGORY_ID, id)
    )
  );

  return results
    .filter(
      (r): r is PromiseFulfilledResult<Awaited<ReturnType<typeof apiClient.productDetail>>> =>
        r.status === 'fulfilled'
    )
    .map((r) => ({
      product_id: r.value.id,
      name: r.value.name,
      price: r.value.price_min,
      image_url: r.value.primary_image_url ?? undefined,
    }));
}

// ─── Sub-components ───────────────────────────────────────────────────────────

function ProductCardSkeleton() {
  return (
    <div className="flex items-center gap-3 p-3 bg-white rounded-2xl border border-zinc-100 animate-pulse">
      <div className="w-14 h-14 rounded-xl bg-zinc-200 flex-shrink-0" />
      <div className="flex-1 space-y-2">
        <div className="h-3 bg-zinc-200 rounded-full w-3/4" />
        <div className="h-3 bg-zinc-200 rounded-full w-1/3" />
      </div>
      <div className="w-4 h-4 bg-zinc-200 rounded-full flex-shrink-0" />
    </div>
  );
}

function ProductCardItem({
  product,
  onClick,
}: {
  product: ProductCard;
  onClick: (id: string) => void;
}) {
  return (
    <button
      onClick={() => onClick(product.product_id)}
      className="w-full flex items-center gap-3 p-3 bg-white rounded-2xl border border-zinc-100 shadow-sm hover:shadow-md hover:border-zinc-300 transition-all group text-left"
    >
      {/* Image */}
      <div className="w-14 h-14 rounded-xl bg-zinc-100 overflow-hidden flex-shrink-0">
        {product.image_url ? (
          <img
            src={product.image_url}
            alt={product.name}
            className="w-full h-full object-cover"
          />
        ) : (
          <div className="w-full h-full flex items-center justify-center text-zinc-400">
            <ShoppingCart className="w-5 h-5" />
          </div>
        )}
      </div>

      {/* Info */}
      <div className="flex-1 min-w-0">
        <p className="text-sm font-semibold text-zinc-800 truncate group-hover:text-zinc-900">
          {product.name}
        </p>
        <p className="text-sm font-bold text-zinc-900 mt-0.5">
          {formatVND(product.price)}
        </p>
      </div>

      {/* Arrow */}
      <ChevronRight className="w-4 h-4 text-zinc-300 group-hover:text-zinc-600 flex-shrink-0 transition-colors" />
    </button>
  );
}

function BotMessage({
  message,
  onProductClick,
}: {
  message: Message;
  onProductClick: (id: string) => void;
}) {
  return (
    <div className="flex justify-start">
      <div className="max-w-[90%] space-y-2">
        {/* Text bubble */}
        {message.content && (
          <div className="p-4 rounded-3xl rounded-tl-none text-sm font-medium bg-white text-zinc-800 border border-zinc-100 shadow-sm whitespace-pre-wrap">
            {message.content}
          </div>
        )}

        {/* Skeletons while loading */}
        {message.isLoadingProducts && (
          <div className="space-y-2">
            {Array.from({ length: MAX_PRODUCT_CARDS }).map((_, i) => (
              <ProductCardSkeleton key={i} />
            ))}
          </div>
        )}

        {/* Loaded product cards */}
        {!message.isLoadingProducts && message.products && message.products.length > 0 && (
          <div className="space-y-2">
            {message.products.map((p) => (
              <ProductCardItem key={p.product_id} product={p} onClick={onProductClick} />
            ))}
          </div>
        )}
      </div>
    </div>
  );
}

// ─── Main Component ───────────────────────────────────────────────────────────

export default function ChatWidget({ setPage, setProductId, setCategoryId }: ChatWidgetProps) {
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [isOpen, setIsOpen] = useState(false);
  const [messages, setMessages] = useState<Message[]>([
    { role: 'bot', content: 'Xin chào! Tôi có thể giúp gì cho bạn hôm nay?' },
  ]);
  const [input, setInput] = useState('');
  const [conversationId, setConversationId] = useState<string | null>(null);
  const [isSending, setIsSending] = useState(false);

  const messagesEndRef = useRef<HTMLDivElement | null>(null);
  const messagesContainerRef = useRef<HTMLDivElement | null>(null);
  const [showScrollBtn, setShowScrollBtn] = useState(false);

  // Navigate to detail page and close the widget
  const handleProductClick = (productId: string) => {
    setProductId(productId);
    setCategoryId(SMARTPHONE_CATEGORY_ID);
    setPage('detail');
    setIsOpen(false);
  };

  const handleSend = async () => {
    const message = input.trim();
    if (!message || isSending) return;

    setIsSending(true);
    setMessages((prev) => [...prev, { role: 'user', content: message }]);
    setInput('');

    try {
      let currentConversationId = conversationId;

      if (!currentConversationId) {
        const conversationResponse = await apiClient.createConversation({ title: '' });
        currentConversationId =
          conversationResponse.data['conversation-service-response']._id;

        if (!currentConversationId) throw new Error('Cannot create conversation');
        setConversationId(currentConversationId);
      }

      const response = await apiClient.sendMessage(currentConversationId, { content: message });
      const serviceResponse = response.data['message-service-response'];
      const botContent = serviceResponse.bot_message.content;
      const productIds = serviceResponse.product_ids ?? [];

      const hasProducts = productIds.length > 0;

      // Show bot text immediately + skeletons if products incoming
      setMessages((prev) => [
        ...prev,
        { role: 'bot', content: botContent, isLoadingProducts: hasProducts, products: [] },
      ]);

      // Fetch top 3 product details in parallel, then patch last message
      if (hasProducts) {
        const cards = await fetchProductCards(productIds);
        setMessages((prev) => {
          const updated = [...prev];
          const lastIdx = updated.length - 1;
          updated[lastIdx] = { ...updated[lastIdx], isLoadingProducts: false, products: cards };
          return updated;
        });
      }
    } catch (error) {
      console.error('Chat error:', error);
      setMessages((prev) => [
        ...prev,
        { role: 'bot', content: 'Có lỗi xảy ra. Vui lòng thử lại.' },
      ]);
    } finally {
      setIsSending(false);
    }
  };

  useEffect(() => {
    const checkAuth = () => setIsAuthenticated(apiClient.isAuthenticated());
    checkAuth();
    window.addEventListener('auth-change', checkAuth);
    return () => window.removeEventListener('auth-change', checkAuth);
  }, []);

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  useEffect(() => {
    if (isOpen) {
      setTimeout(() => {
        messagesEndRef.current?.scrollIntoView({ behavior: 'instant' });
      }, 300); // wait for open animation to finish
    }
  }, [isOpen]);

  if (!isAuthenticated) return null;

  return (
    <div className="fixed bottom-8 right-8 z-[1000]">
      {/* Toggle Button */}
      <button
        onClick={() => setIsOpen(!isOpen)}
        className="w-16 h-16 bg-zinc-900 text-white rounded-full flex items-center justify-center shadow-2xl hover:scale-110 active:scale-95 transition-all group"
      >
        {isOpen ? (
          <X className="w-6 h-6" />
        ) : (
          <MessageSquare className="w-6 h-6 group-hover:rotate-12 transition-transform" />
        )}
        {!isOpen && (
          <span className="absolute -top-1 -right-1 w-5 h-5 bg-[#ba1a1a] rounded-full border-4 border-white" />
        )}
      </button>

      {/* Chat Window */}
      <AnimatePresence>
        {isOpen && (
          <motion.div
            initial={{ opacity: 0, y: 20, scale: 0.9 }}
            animate={{ opacity: 1, y: 0, scale: 1 }}
            exit={{ opacity: 0, y: 20, scale: 0.9 }}
            className="absolute bottom-20 right-0 w-[400px] max-w-[calc(100vw-2rem)] bg-white rounded-[2.5rem] shadow-[0_20px_70px_-10px_rgba(0,0,0,0.2)] border border-zinc-100 overflow-hidden flex flex-col"
          >
            {/* Header */}
            <div className="p-6 bg-zinc-900 text-white">
              <div className="flex items-center gap-3">
                <div className="w-10 h-10 rounded-2xl bg-[#FFD194] flex items-center justify-center text-zinc-900">
                  <Bot className="w-5 h-5" />
                </div>
                <div>
                  <h3 className="font-black uppercase tracking-widest text-xs">WiseTech Assistant</h3>
                  <div className="flex items-center gap-1.5 pt-0.5">
                    <span className="w-1.5 h-1.5 bg-green-400 rounded-full animate-pulse" />
                    <span className="text-[10px] font-bold text-zinc-400">Online now</span>
                  </div>
                </div>
              </div>
            </div>

            {/* Messages */}
            <div
              ref={messagesContainerRef}
              onScroll={() => {
                const el = messagesContainerRef.current;
                if (!el) return;
                setShowScrollBtn(el.scrollHeight - el.scrollTop - el.clientHeight > 80);
              }}
              className="flex-1 p-4 space-y-4 max-h-[420px] overflow-y-auto bg-zinc-50/50 scrollbar-hide relative"
            >
              {messages.map((msg, idx) =>
                msg.role === 'bot' ? (
                  <BotMessage key={idx} message={msg} onProductClick={handleProductClick} />
                ) : (
                  <div key={idx} className="flex justify-end">
                    <div className="max-w-[80%] p-4 rounded-3xl rounded-tr-none text-sm font-medium bg-zinc-900 text-white">
                      {msg.content}
                    </div>
                  </div>
                )
              )}

              {/* Typing indicator */}
              {isSending && (
                <div className="flex justify-start">
                  <div className="p-4 rounded-3xl rounded-tl-none bg-white border border-zinc-100 shadow-sm flex gap-1.5 items-center">
                    {[0, 1, 2].map((i) => (
                      <span
                        key={i}
                        className="w-2 h-2 bg-zinc-300 rounded-full animate-bounce"
                        style={{ animationDelay: `${i * 150}ms` }}
                      />
                    ))}
                  </div>
                </div>
              )}

              {showScrollBtn && (
                <div className="sticky bottom-2 flex justify-center">
                  <button
                    onClick={() => messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' })}
                    className="w-8 h-8 bg-zinc-900/70 backdrop-blur-sm text-white rounded-full shadow-lg hover:bg-zinc-900 transition-all flex items-center justify-center"
                  >
                    <ChevronRight className="w-4 h-4 rotate-90" />
                  </button>
                </div>
              )}

              <div ref={messagesEndRef} />
            </div>

            {/* Input */}
            <div className="p-4 bg-white border-t border-zinc-100">
              <div className="relative flex items-center">
                <input
                  type="text"
                  value={input}
                  onChange={(e) => setInput(e.target.value)}
                  onKeyDown={(e) => {
                    if (e.key === 'Enter') handleSend();
                  }}
                  placeholder="Nhắn tin cho WiseTech..."
                  className="w-full pl-6 pr-14 py-4 bg-zinc-100 rounded-2xl border-none outline-none font-medium text-xs focus:ring-2 focus:ring-zinc-900 transition-all"
                />
                <button
                  onClick={handleSend}
                  disabled={isSending}
                  className="absolute right-2 p-2 bg-zinc-900 text-white rounded-xl hover:bg-zinc-800 transition-all active:scale-90 disabled:opacity-50"
                >
                  <Send className="w-4 h-4" />
                </button>
              </div>
            </div>
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  );
}
