import { NextResponse } from 'next/server';
import { createClient } from '@supabase/supabase-js';

const supabaseUrl = process.env.NEXT_PUBLIC_SUPABASE_URL;
const serviceRoleKey = process.env.SUPABASE_SERVICE_ROLE_KEY;

export async function POST(request: Request) {
  if (!supabaseUrl || !serviceRoleKey) {
    return NextResponse.json(
      {
        success: false,
        error: 'Server registration is not configured. Set SUPABASE_SERVICE_ROLE_KEY to enable account creation without email verification.',
      },
      { status: 500 }
    );
  }

  const body = await request.json().catch(() => null);
  const email = typeof body?.email === 'string' ? body.email.trim() : '';
  const password = typeof body?.password === 'string' ? body.password : '';

  if (!email || !password) {
    return NextResponse.json(
      { success: false, error: 'Email and password are required.' },
      { status: 400 }
    );
  }

  const supabase = createClient(supabaseUrl, serviceRoleKey, {
    auth: {
      autoRefreshToken: false,
      persistSession: false,
      detectSessionInUrl: false,
    },
  });

  const { data, error } = await supabase.auth.admin.createUser({
    email,
    password,
    email_confirm: true,
  });

  if (error) {
    const message = error.message.toLowerCase();
    const status = message.includes('already registered') ? 409 : 400;
    return NextResponse.json(
      { success: false, error: error.message },
      { status }
    );
  }

  return NextResponse.json({
    success: true,
    user: data.user,
  });
}