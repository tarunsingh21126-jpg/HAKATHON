import { Link } from 'react-router-dom';
import { Package, Leaf, Recycle } from 'lucide-react';

export default function Home() {
  return (
    <div className="max-w-6xl mx-auto space-y-24 py-12">
      {/* Hero Section */}
      <section className="text-center space-y-6">
        <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-brand-100 text-brand-700 text-sm font-medium mb-4">
          <Leaf className="w-4 h-4" /> Eco-friendly Delivery
        </div>
        <h1 className="text-5xl md:text-7xl font-extrabold tracking-tight text-slate-900">
          Reusable Packaging.<br/>
          <span className="text-transparent bg-clip-text bg-gradient-to-r from-brand-600 to-accent-500">
            Zero Waste.
          </span>
        </h1>
        <p className="text-xl text-slate-600 max-w-2xl mx-auto leading-relaxed">
          PackBack is a QR-powered reusable packaging platform that connects customers, local sellers, and return networks to keep delivery packaging in circulation.
        </p>
        <div className="pt-4 flex items-center justify-center gap-4">
          <Link to="/register" className="px-8 py-3.5 bg-brand-600 text-white rounded-xl font-medium text-lg hover:bg-brand-700 shadow-lg shadow-brand-500/30 transition-all hover:-translate-y-1">
            Join as Customer
          </Link>
          <Link to="/register?role=seller" className="px-8 py-3.5 bg-white text-slate-700 border border-slate-200 rounded-xl font-medium text-lg hover:bg-slate-50 transition-all">
            Partner as Seller
          </Link>
        </div>
      </section>

      {/* How it Works */}
      <section className="grid md:grid-cols-3 gap-8 px-4">
        <div className="bg-white p-8 rounded-2xl shadow-sm border border-slate-100 text-center space-y-4">
          <div className="w-16 h-16 bg-brand-50 text-brand-600 rounded-2xl flex items-center justify-center mx-auto mb-6">
            <Package className="w-8 h-8" />
          </div>
          <h3 className="text-xl font-bold">1. Receive Order</h3>
          <p className="text-slate-500">Your order arrives in a durable, reusable PackBack container.</p>
        </div>
        <div className="bg-white p-8 rounded-2xl shadow-sm border border-slate-100 text-center space-y-4">
          <div className="w-16 h-16 bg-accent-50 text-accent-600 rounded-2xl flex items-center justify-center mx-auto mb-6">
            <ScanLine className="w-8 h-8" />
          </div>
          <h3 className="text-xl font-bold">2. Scan QR</h3>
          <p className="text-slate-500">Scan the QR code to request a pickup or find a drop-off point.</p>
        </div>
        <div className="bg-white p-8 rounded-2xl shadow-sm border border-slate-100 text-center space-y-4">
          <div className="w-16 h-16 bg-brand-50 text-brand-600 rounded-2xl flex items-center justify-center mx-auto mb-6">
            <Recycle className="w-8 h-8" />
          </div>
          <h3 className="text-xl font-bold">3. Return & Earn</h3>
          <p className="text-slate-500">Get your deposit back and earn rewards for returning packaging.</p>
        </div>
      </section>
    </div>
  );
}

function ScanLine(props) {
  return (
    <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" {...props}>
      <path d="M3 7V5a2 2 0 0 1 2-2h2"></path>
      <path d="M17 3h2a2 2 0 0 1 2 2v2"></path>
      <path d="M21 17v2a2 2 0 0 1-2 2h-2"></path>
      <path d="M7 21H5a2 2 0 0 1-2-2v-2"></path>
      <line x1="7" y1="12" x2="17" y2="12"></line>
    </svg>
  );
}
