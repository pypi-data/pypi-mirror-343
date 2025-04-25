import numpy as np
from scipy.optimize import minimize
from sklearn.metrics.pairwise import pairwise_kernels
from .func import estimate_E_Z_given_X, estimate_h_functions, compute_beta_se, compute_beta_se_noncensor

def genius_censor(X, Z, A, Y, censor_delta, h=1,
                  config_nn={
                      'hidden_layers': [50,50],
                      'learning_rate': 0.0005,
                      'weight_decay': 0.0001,
                      'batch_size': 256,
                      'dropout_rate': 0,
                      'patience': 5,
                      'epochs': 100,
                      'validation_split': 0.05,
                      'shuffle': False,
                      'device': 'cpu'
                  },
                  model_types=['neural_network'],
                  rho_function_names=['ET']):
   """
   For each combination of model_type and rho function, estimate beta, SE, and test statistic.
   Returns a nested dict results[model_type][rho] = {'beta':..., 'se':..., 'test':...}
   """
   # 90/10 split
   n = Z.shape[0]
   m = Z.shape[1]
   n_train = int(n*0.9)
   idx1 = np.arange(n_train)
   idx2 = np.arange(n_train, n)
   X_train, Z_train, A_train, Y_train, censor_train = X[idx1], Z[idx1], A[idx1], Y[idx1], censor_delta[idx1]
   X_est, Z_est, A_est, Y_est, censor_est = X[idx2], Z[idx2], A[idx2], Y[idx2], censor_delta[idx2]

   # Kernel & weight matrix
   OA_i = np.hstack((A_train[:,None], X_train, Z_train))
   OA_j = np.hstack((A_est[:,None], X_est, Z_est))
   K = pairwise_kernels(OA_i, OA_i, metric='rbf', gamma=2/h**2,n_jobs=-1)
   B = K/np.sum(K,axis=0)

   def compute_Gn():
       mask_y = (Y_train[:,None] <= Y_train[None,:])
       mask_y_delta = mask_y*(1-censor_train[:,None])
       H = mask_y.dot(B)
       H = np.maximum(H,0.01)
       Gn = np.ones(n_train)
       for j in range(n_train):
           temp = (1 - B[j]/H[j])
           Gn *= temp**mask_y_delta[j]
       return np.maximum(Gn,0.01)

   Gn = compute_Gn()
   IPW = censor_train/Gn

   def compute_Phi():
       Kji = pairwise_kernels(OA_j, OA_i, metric='rbf', gamma=0.1,n_jobs=-1)
       Bji = Kji/np.sum(Kji,axis=0)
       mask_est = (Y_est[:,None] <= Y_est[None,:])
       mask_ji = (Y_est[:,None] <= Y_train[None,:])*(1-censor_est[:,None])
       Hji = mask_est.dot(Bji)
       Hji = np.maximum(Hji,0.1)
       term1 = np.zeros_like(Bji)
       delta_mask = (censor_est==0)
       for k in range(len(Y_est)):
           min_mask = (Y_est[k]<=Y_est[:,None])&(Y_est[k]<=Y_train[None,:])
           temp = Bji[k]/Hji[k]**2
           term1 += temp*min_mask*delta_mask[:,None]
       return Bji*Gn[None,:]*(mask_ji/Hji - term1)

   Phi = compute_Phi()

   rho_funcs = {
       'ET': lambda v: -np.exp(v)+1,
       'EL': lambda v: np.log(1-v),
       'CUE': lambda v: -v - v**2/2
   }
   rho_derivatives = {
        'ET': {
            'rho': lambda v: np.sum(-np.exp(v) + 1),
            'rho_prime': lambda v: -np.exp(v),
            'rho_double_prime': lambda v: -np.exp(v),
        },
        'EL': {
            'rho': lambda v: np.sum(np.log(1 - v)),
            'rho_prime': lambda v: -1 / (1 - v),
            'rho_double_prime': lambda v: -1 / (1 - v) ** 2,
        },
        'CUE': {
            'rho': lambda v: np.sum(-v - v ** 2 / 2),
            'rho_prime': lambda v: -1 - v,
            'rho_double_prime': lambda v: -np.ones_like(v),
        },
    }

   results = {}

   for model in model_types:
       EZ = estimate_E_Z_given_X(X_train,Z_train,config_nn,model)
       RA,RY,h3,h4 = estimate_h_functions(X_train,Z_train,A_train,Y_train,config_nn,model)
       def compute_g(beta):
           b=beta[0]
           Delta=(RA*RY - b*RA**2)-(h3-b*h4)
           g=(Z_train - EZ)*Delta[:,None]
           g_d1=-(Z_train-EZ)*(RA**2-h4)[:,None]
           return g,g_d1
       results[model] = {}
       for rho_name in rho_function_names:
           def Q(beta):
               g,g_d1 = compute_g(beta)
               xi = B.T.dot(IPW[:,None]*g)
               psi = IPW[:,None]*(g-xi)+xi
               Sigma = psi.T.dot(psi)/psi.shape[0]
               Sigma_inv = np.linalg.pinv(Sigma+np.eye(Sigma.shape[0])*1e-3)
               lam = -psi.mean(0).dot(Sigma_inv)
               lam_psi=psi.dot(lam)
               if rho_name=='EL': lam_psi = np.minimum(0.9, lam_psi)
               Q_value = rho_funcs[rho_name](lam_psi).mean()
               return Q_value

           res = minimize(Q, np.random.rand(1), method='Powell', bounds=[(-10,10)])
           beta_hat=res.x[0]
           ghat,g_d1=compute_g(res.x)
           xi= B.T.dot(IPW[:,None]*ghat)
           xi_d1=B.T.dot(IPW[:,None]*g_d1)
           SE,VarQ= compute_beta_se(ghat,g_d1,Phi,IPW,Gn,xi,xi_d1,rho_derivatives,rho_name)
           tempQ = 2*n_train*Q(res.x)
           test=(tempQ - m)/np.sqrt(2*m*(1+VarQ))
           results[model][rho_name]={'beta':beta_hat,'se':SE,'test':test}

   return results


def genius_noncensor(X, Z, A, Y,
                  config_nn={
                      'hidden_layers': [50,50],
                      'learning_rate': 0.0005,
                      'weight_decay': 0.0001,
                      'batch_size': 256,
                      'dropout_rate': 0,
                      'patience': 5,
                      'epochs': 100,
                      'validation_split': 0.05,
                      'shuffle': False,
                      'device': 'cpu'
                  },
                  model_types=['neural_network'],
                  rho_function_names=['ET']):
   """
   For each combination of model_type and rho function, estimate beta, SE, and test statistic.
   Returns a nested dict results[model_type][rho] = {'beta':..., 'se':..., 'test':...}
   """
   n_train = Z.shape[0]
   m = Z.shape[1]
   X_train, Z_train, A_train, Y_train = X, Z, A, Y

   rho_funcs = {
       'ET': lambda v: -np.exp(v)+1,
       'EL': lambda v: np.log(1-v),
       'CUE': lambda v: -v - v**2/2
   }
   rho_derivatives = {
        'ET': {
            'rho': lambda v: np.sum(-np.exp(v) + 1),
            'rho_prime': lambda v: -np.exp(v),
            'rho_double_prime': lambda v: -np.exp(v),
        },
        'EL': {
            'rho': lambda v: np.sum(np.log(1 - v)),
            'rho_prime': lambda v: -1 / (1 - v),
            'rho_double_prime': lambda v: -1 / (1 - v) ** 2,
        },
        'CUE': {
            'rho': lambda v: np.sum(-v - v ** 2 / 2),
            'rho_prime': lambda v: -1 - v,
            'rho_double_prime': lambda v: -np.ones_like(v),
        },
    }

   results = {}


   for model in model_types:
       EZ = estimate_E_Z_given_X(X_train,Z_train,config_nn,model)
       RA,RY,h3,h4 = estimate_h_functions(X_train,Z_train,A_train,Y_train,config_nn,model)
       def compute_g(beta):
           b=beta[0]
           Delta=(RA*RY - b*RA**2)-(h3-b*h4)
           g=(Z_train - EZ)*Delta[:,None]
           g_d1=-(Z_train-EZ)*(RA**2-h4)[:,None]
           return g,g_d1
       results[model] = {}
       for rho_name in rho_function_names:
           def Q(b):
               g,g_d1 = compute_g(b)
               Omega = g.T.dot(g)/g.shape[0]
               inv = np.linalg.pinv(Omega+np.eye(Omega.shape[0])*1e-3)
               lam = -g.mean(0).dot(inv)
               lam_psi=g.dot(lam)
               if rho_name=='EL': lam_psi = np.minimum(0.9, lam_psi)
               return rho_funcs[rho_name](lam_psi).mean()

           res = minimize(Q, np.random.rand(1), method='Powell', bounds=[(-10,10)])
           beta_hat=res.x[0]
           ghat,g_d1=compute_g(res.x)
           SE= compute_beta_se_noncensor(ghat, g_d1, rho_derivatives, rho_name)
           tempQ = 2*n_train*Q(res.x)
           test=(tempQ - m)/np.sqrt(2*m)
           results[model][rho_name]={'beta':beta_hat,'se':SE,'test':test}

   return results

