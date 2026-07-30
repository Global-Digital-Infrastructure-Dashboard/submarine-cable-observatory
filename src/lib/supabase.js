import { createClient } from '@supabase/supabase-js'

const supabaseUrl = 'https://nvlvwmkpaunoudvoivrz.supabase.co'  
const supabaseKey = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Im52bHZ3bWtwYXVub3Vkdm9pdnJ6Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzQzODMyMTEsImV4cCI6MjA4OTk1OTIxMX0.WrXp2LD9TPQdnw-IXXIoKwm1UXzCgjJqtEFNaH3rkb4'

export const supabase = createClient(supabaseUrl, supabaseKey)