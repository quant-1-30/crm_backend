# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["http://localhost:3000"],  # 允许的源
#     allow_credentials=True,  # 允许携带凭证
#     allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],  # 允许的 HTTP 方法
#     allow_headers=[
#         "Content-Type",
#         "Authorization",
#         "Accept",
#         "Origin",
#         "X-Requested-With",
#     ],  # 允许的请求头
#     expose_headers=["Content-Length", "X-Custom-Header"],  # 允许浏览器访问的响应头
#     max_age=3600,  # 预检请求的缓存时间（秒）
# )
